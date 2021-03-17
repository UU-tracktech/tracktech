import json
import tornado.web
from tornado import httputil
from tornado.websocket import WebSocketHandler
from objectManager import objects
import client

class ProcessorSocket(WebSocketHandler):

    def __init__(
            self,
            application: tornado.web.Application,
            request: httputil.HTTPServerRequest
    ):
        super().__init__(application, request)
        self.identifier = max(processors.keys(), default=0) + 1

    # CORS
    def check_origin(self, origin):
        return True

    # Append self to processor dict upon opening
    def open(self):
        print(f"New processor connected with id: {self.identifier}")
        processors[self.identifier] = self

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        try:
            # Handle all message types
            message_object = json.loads(message)
            if message_object["type"] == "boundingBoxes":
                send_bounding_boxes(message_object, self.identifier)
            elif message_object["type"] == "featureMap":
                update_feature_map(message_object)
            else:
                print("Someone gave an unknown command")
        except ValueError:
            print("Someone wrote bad json")
        except KeyError:
            print("Someone missed a property in their json")

    def on_close(self):
        del processors[self.identifier]
        print("Processor WebSocket closed")


# Send bounding boxes to all clients
def send_bounding_boxes(message, camera_id):
    frame_id = message["frameId"]
    boxes = message["boxes"]

    if len(client.clients) > 0:
        for c in client.clients:
            c.write_message(json.dumps({
                "type": "boundingBoxes",
                "cameraId": camera_id,
                "frameId": frame_id,
                "boxes": boxes
            }))


# Send updated feature map to all processors
def update_feature_map(message):
    object_id = message["objectId"]
    feature_map = message["featureMap"]

    try:
        objects[object_id].update_feature_map(feature_map)
    except KeyError:
        print("Unknown object id")

    for p in processors.values():
        p.write_message(json.dumps({
            "type": "featureMap",
            "objectId": object_id,
            "featureMap": feature_map
        }))


processors = dict()
