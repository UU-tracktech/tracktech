import json
from tornado.websocket import WebSocketHandler


class ProcessorSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        processors.append(self)

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        try:
            message_object = json.loads(message)
            if message_object["type"] == "featureMap":
                update_feature_map(message_object)
            else:
                for p in processors:
                    p.write_message("Someone gave an unknown command")
        except ValueError:
            for p in processors:
                p.write_message("Someone wrote bad json")
        except KeyError:
            for p in processors:
                p.write_message("Someone missed a property in their json")

    def on_close(self):
        print("Processor WebSocket closed")


def update_feature_map(message):
    object_id = message["objectId"]
    feature_map = message["featureMap"]
    for p in processors:
        p.write_message(f"Someone send a feature map of an object with Id {object_id}")


processors: list[ProcessorSocket] = []
