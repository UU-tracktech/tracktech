from typing import List, Any

from tornado.websocket import WebSocketHandler

class ClientSocket(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        clients.append(self)

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        for c in clients:
            c.write_message(u"Someone said: " + message)

    def on_close(self):
        print("WebSocket closed")


clients: list[ClientSocket] = []
