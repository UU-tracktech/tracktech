import json
import tornado.web
from time import sleep
from tornado import httputil
from tornado.websocket import WebSocketHandler
from objectManager import TrackingObject, objects
from processor import processors


class ClientSocket(WebSocketHandler):

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest):
        super().__init__(application, request)
        self.identifier = max(clients.keys(), default=0) + 1

    # CORS
    def check_origin(self, origin):
        return True

    # Append self to client list upon opening
    def open(self):
        print(f"New client connected with id: {self.identifier}")
        clients[self.identifier] = self

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        try:
            message_object = json.loads(message)

            # Switch on message type
            actions = {
                "start":
                    lambda: start_tracking(message_object),
                "stop":
                    lambda: stop_tracking(message_object),
                "test":
                    lambda: send_mock_data(message_object, self)
            }

            # Execute correct function
            function = actions.get(message_object["type"])
            if function is None:
                print("Someone gave an unknown command")
            else:
                function()

        except ValueError:
            print("Someone wrote bad json")
        except KeyError:
            print("Someone missed a property in their json")

    def on_close(self):
        del clients[self.identifier]
        print(f"Client with id {self.identifier} disconnected")


# Create tracking object and send start tracking command to specified processor
def start_tracking(message):
    camera_id = message["cameraId"]
    box_id = message["boxId"]
    frame_id = message["frameId"]

    if camera_id not in processors.keys():
        print("Unknown processor")
        return

    tracking_object = TrackingObject()

    print(
        f"New tracking object created with id {tracking_object.identifier}, found at bounding box with Id {box_id} on "
        f"frame {frame_id} of camera {camera_id}")

    processors[camera_id].write_message(json.dumps({
        "type": "start",
        "objectId": tracking_object.identifier,
        "frameId": frame_id,
        "boxId": box_id
    }))


# Remove tracking object and send stop tracking command to all processors
def stop_tracking(message):
    object_id = message["objectId"]
    if object_id not in objects.keys():
        print("unknown object")
        return

    objects[object_id].remove_self()

    if len(processors) > 0:
        for p in processors.values():
            p.write_message(json.dumps({
                "type": "stop",
                "objectId": object_id
            }))

    print(f"stopped tracking of object with id {object_id}")


# Send a few mock messages to the client for testing purposes
def send_mock_data(message, client):
    camera_id = message["cameraId"]

    frame_id = 0

    for x in range(50):
        client.write_message(json.dumps({
            "type": "boundingBoxes",
            "cameraId": camera_id,
            "frameId": frame_id,
            "boxes": {}
        }))

        frame_id += 1
        sleep(0.2)


clients = dict()
