import json
import tornado.web
from time import sleep
from tornado import httputil
from tornado.websocket import WebSocketHandler
from objectManager import objects, TrackingObject
import client
import logger


class ProcessorSocket(WebSocketHandler):

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest):
        super().__init__(application, request)
        self.identifier = max(processors.keys(), default=0) + 1

    # CORS
    def check_origin(self, origin):
        return True

    # Append self to processor dict upon opening
    def open(self):
        logger.log_connect("/processor", self.request.remote_ip)
        print(f"New processor connected with id: {self.identifier}")
        processors[self.identifier] = self

    def on_message(self, message):
        logger.log_message_receive(message, "/processor", self.request.remote_ip)

        try:
            message_object = json.loads(message)

            # Switch on message type
            actions = {
                "boundingBoxes":
                    lambda: send_bounding_boxes(message_object, self.identifier),
                "featureMap":
                    lambda: update_feature_map(message_object),
                "test":
                    lambda: send_mock_commands(message_object, self)
            }

            # Execute correct function
            function = actions.get(message_object["type"])
            if function is None:
                print("Someone gave an unknown command")
            else:
                function()

        except ValueError:
            logger.log_error("/processor", "ValueError", self.request.remote_ip)
            print("Someone wrote bad json")
        except KeyError:
            logger.log_error("/processor", "KeyError", self.request.remote_ip)
            print("Someone missed a property in their json")

    def send_message(self, message):
        logger.log_message_send(message, "/processor", self.request.remote_ip)
        self.write_message(message)

    def on_close(self):
        logger.log_disconnect("/processor", self.request.remote_ip)
        del processors[self.identifier]
        print(f"Processor with id {self.identifier} disconnected")


# Send bounding boxes to all clients
def send_bounding_boxes(message, camera_id):
    frame_id = message["frameId"]
    boxes = message["boxes"]

    if len(client.clients.values()) > 0:
        for c in client.clients.values():
            c.send_message(json.dumps({
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
        p.send_message(json.dumps({
            "type": "featureMap",
            "objectId": object_id,
            "featureMap": feature_map
        }))


# Send a few mock messages to the processor for testing purposes
def send_mock_commands(message, processor):
    frame_id = message["frameId"]
    box_id = message["boxId"]
    tracking_object1 = TrackingObject()

    tracking_object2 = TrackingObject()

    processor.send_message(json.dumps({
        "type": "start",
        "objectId": tracking_object1.identifier,
        "frameId": frame_id,
        "boxId": box_id
    }))

    sleep(2)

    processor.send_message(json.dumps({
        "type": "featureMap",
        "objectId": tracking_object2.identifier,
        "featureMap": {}
    }))

    sleep(2)

    processor.send_message(json.dumps({
        "type": "stop",
        "objectId": tracking_object1.identifier
    }))


processors = dict()
