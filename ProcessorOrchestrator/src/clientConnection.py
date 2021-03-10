from typing import List, Any

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

class ClientSocket(WebSocketHandler):
    tagDescription = dict(name="Client",
                          description="Client websocket can be found at \"/client\", this socket is used to send "
                                      "tracking information")

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

class ClientStartTracking(RequestHandler):

    def post(self):
        """ Start tracking of individual
        ---
        tags: [Client]
        summary: Start the tracking of an object
        description: Takes camera id and bounding box id and sends a command to start tracking that object
        responses:
            200:
                description: OK
                content:
                    text/plain:
                        schema:
                            type: string
                            example: pong
        """
        self.write("Nothing happened yet")

clients: list[ClientSocket] = []
