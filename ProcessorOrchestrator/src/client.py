from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
import json


class ClientSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        try:
            message_object = json.loads(message)
            if message_object["type"] == "start":
                start_tracking(message_object)
            elif message_object["type"] == "stop":
                start_tracking(message_object)
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


def start_tracking(message):
    camera_id = message["cameraId"]
    box_id = message["boxId"]
    frame_id = message["frameId"]

    for c in clients:
        c.write_message(
            f"Someone wanted to start tracking box with Id {box_id} on frame {frame_id} of camera {camera_id}")


def stop_tracking(message):
    object_id = message["objectId"]

    for c in clients:
        c.write_message(f"You wanted to stop tracking object with Id {object_id}")


clients: list[ClientSocket] = []
