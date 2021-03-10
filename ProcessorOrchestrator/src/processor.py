from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

class ProcessorSocket(WebSocketHandler):
    tagDescription = dict(name="Processor",
                          description="Processor websocket can be found at \"/processor\", this socket is used to send "
                                      "tracking information")

    def check_origin(self, origin):
        return True

    def open(self):
        processors.append(self)

    def send(self, message):
        self.write_message(message)

    def on_message(self, message):
        for p in processors:
            p.write_message(u"A processor sent: " + message)

    def on_close(self):
        print("Processor WebSocket closed")

class ProcessorFeatureMap(RequestHandler):

    def check_origin(self, origin):
        return True

    def post(self):
        """ Adds or updates feature map of tracked object
        ---
        tags: [Processor]
        summary: Adds or updates feature map of tracked object
        description: Takes object id and feature map and sends a command to start tracking that object
        parameters:
            -   in: body
                name: feature map
                description: Object id and feature map
                schema:
                    type: object
                    required:
                        -   objectId
                        -   featureMap
                    properties:
                        objectId:
                            type: integer
                        featureMap:
                            type: object
        responses:
            200:
                description: OK
        """
        object_id = self.get_body_argument("objectId")
        feature_map = self.get_body_argument("featureMap")
        self.write(f"You send a feature map of an object with Id {object_id}")

processors: list[ProcessorSocket] = []