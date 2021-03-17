from tornado.websocket import WebSocketHandler
from objectManager import TrackingObject, objects
from processor import processors
import json

from typing import List


class ClientSocket(WebSocketHandler):

    # CORS
    def check_origin(self, origin):
        return True

    # Append self to client list upon opening
    def open(self):
        clients.append(self)

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        try:
            # Handle all message types
            message_object = json.loads(message)
            if message_object["type"] == "start":
                start_tracking(message_object)
            elif message_object["type"] == "stop":
                stop_tracking(message_object)
            else:
                for c in clients:
                    c.write_message("Someone gave an unknown command")
        except ValueError:
            for c in clients:
                c.write_message("Someone wrote bad json")
        except KeyError:
            for c in clients:
                c.write_message("Someone missed a property in their json")

    def on_close(self):
        print("WebSocket closed")


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


clients: List[ClientSocket] = []
