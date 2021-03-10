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


class ClientTracking(RequestHandler):

    def check_origin(self, origin):
        return True

    def post(self):
        """ Start tracking of individual
        ---
        tags: [Client]
        summary: Start the tracking of an object
        description: Takes camera id and bounding box id and sends a command to start tracking that object
        parameters:
            -   in: body
                name: command
                description: Parameters for the command to be executed
                schema:
                    type: object
                    required:
                        -   cameraId
                        -   boxId
                        -   frameId
                    properties:
                        cameraId:
                            type: integer
                        boxId:
                            type: integer
                        frameId:
                            type: integer
        responses:
            200:
                description: OK
        """
        camera_id = self.get_body_argument("cameraId")
        box_id = self.get_body_argument("boxId")
        frame_id = self.get_body_argument("frameId")
        self.write(f"You wanted to start tracking box with Id {box_id} on frame {frame_id} of camera {camera_id}")


    def delete(self):
        """ Stop tracking of individual
                ---
                tags: [Client]
                summary: Stop the tracking of an object
                description: Takes object id and sends commands to stop tracking that object
                parameters:
                    -   in: body
                        name: command
                        description: Parameters for the command to be executed
                        schema:
                            type: object
                            required:
                                -   objectId
                            properties:
                                boxId:
                                    type: integer
                responses:
                    200:
                        description: OK
                """
        object_id = self.get_body_argument("objectId")
        self.write(f"You wanted to stop tracking object with Id {object_id}")


clients: list[ClientSocket] = []
