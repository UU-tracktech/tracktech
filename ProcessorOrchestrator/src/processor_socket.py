"""Processor component to handle processor websocket connections.

This file contains a websocket class to handle websocket connections coming from camera processors. It defines multiple
functions that can be called using specified json messages.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json
from time import sleep

from tornado.websocket import WebSocketHandler

from src.object_manager import objects, TrackingObject
from src.connections import processors
import src.client_socket as client_socket
import src.logger as logger


class ProcessorSocket(WebSocketHandler):
    """Websocket handler for camera processors.

    Attributes:
        identifier: An int that serves as the unique identifier to this object.
        authorized: A bool that shows whether or not the connection is authorized.
    """

    def __init__(self, application, request):
        """Creates unique id and appends it to the dict of processors.

        Args:
            application (tornado.web.Application): The tornado web application
            request (httputil.HTTPServerRequest): The HTTP server request
        """
        super().__init__(application, request)
        self.identifier = None
        self.authorized = False

        # Load the auth object from appsettings
        self.auth = self.application.settings.get('processor_auth')

    def check_origin(self, origin):
        """Override to enable support for allowing alternate origins.

        Args:
            origin (string):
                Origin of the HTTP request, is ignored as all origins are allowed.
        Returns:
            bool
        """
        return True

    def open(self, *args, **kwargs):
        """Called upon opening of the websocket.

        Method called upon the opening of the websocket, will log connection

        Returns:
            None
        """
        logger.log_connect("/processor", self.request.remote_ip)
        logger.log("New processor connected")

    # pylint: disable=broad-except
    def on_message(self, message):
        """Handles a message from a processor that is received on the websocket.

        Method which handles messages coming in from a processor. The messages are expected in json format.

        Args:
            message (string):
                JSON with at least a "type" property. This property can have the following values:
                    - "boundingBoxes" | This signifies a message that contains bounding boxes, see send_bounding_boxes
                                        for the other expected properties.
                    - "featureMap"    | This signifies a message that contains a feature map of an object,
                                        see update_feature_map, for the other expected properties.
                    - "test"          | This values will be answered with a series of messages mocking the messages
                                        a processor might expect, see send_mock_commands for the other expected
                                        properties.
        Returns:
            None
        """
        logger.log_message_receive(message, "/processor", self.request.remote_ip)

        try:
            message_object = json.loads(message)

            # Switch on message type
            actions = {
                "identifier":
                    lambda: self.register_processor(message_object),
                "boundingBoxes":
                    lambda: self.send_bounding_boxes(message_object),
                "featureMap":
                    lambda: self.update_feature_map(message_object),
                "test":
                    lambda: self.send_mock_commands(message_object)
            }

            action_type = message_object["type"]

            if self.authorized or self.auth is None:
                # Execute correct function
                function = actions.get(action_type)
                if function is None:
                    logger.log("Someone gave an unknown command")
                else:
                    function()
            elif action_type == "authenticate":
                self.authenticate(message_object)
            else:
                logger.log("A processor was not authenticated first")

        except ValueError:
            logger.log_error("/processor", "ValueError", self.request.remote_ip)
            logger.log("Someone wrote bad json")
        except KeyError:
            logger.log_error("/processor", "KeyError", self.request.remote_ip)
            logger.log("Someone missed a property in their json")
        except Exception as exc:
            logger.log_error("/processor", exc, self.request.remote_ip)

    def authenticate(self, message):
        """Authenticates a processor

        Args:
            message (json):
                JSON message that was received. It should contain the following property:
                    - "jwt" | The jwt token containing information about a user
        """

        if self.auth is not None:
            self.auth.validate(message["jwt"])
            self.authorized = True

    def send_message(self, message):
        """Sends a message over the websocket and logs it.

        Args:
            message (string): string which should be send over this websocket
        Returns:
            None
        """
        logger.log_message_send(message, "/processor", self.request.remote_ip)
        self.write_message(message)

    def on_close(self):
        """Called when the websocket is closed, deletes itself from the dict of processors.

        Returns:
            None
        """
        logger.log_disconnect("/processor", self.request.remote_ip)
        del processors[self.identifier]
        logger.log(f"Processor with id {self.identifier} disconnected")

    def data_received(self, chunk):
        """Unused method that could handle streamed request data"""

    def register_processor(self, message) -> None:
        """Registers a processor under the given identifier.

        Args:
            message (json):
                JSON message that was received. It should contain the following property:
                    - "id" | The identifier of the processor under which this socket should be registered.
        """
        identifier = message["id"]

        self.identifier = identifier
        processors[self.identifier] = self

        logger.log(f"Processor registered with id {self.identifier} from {self.request.remote_ip}")
        logger.log(f"Processor registered with id {self.identifier}")

    def send_bounding_boxes(self, message):
        """Sends bounding boxes to all clients.

        Args:
            message (json):
                JSON message that was received. It should contain the following properties:
                    - "frameId" | The identifier of the frame for which these bounding boxes were computed.
                    - "boxes"   | An object containing the bounding boxes that were computed for this frame.
        Returns:
            None
        """
        frame_id = message["frameId"]
        boxes = message["boxes"]

        if len(client_socket.clients.values()) > 0:
            for client in client_socket.clients.values():
                client.send_message(json.dumps({
                    "type": "boundingBoxes",
                    "cameraId": self.identifier,
                    "frameId": frame_id,
                    "boxes": boxes
                }))

    @staticmethod
    def update_feature_map(message):
        """Sends an updated feature map to all processors

        Args:
            message (json):
                JSON message that was received. It should contain the following properties:
                    - "objectId"   | The identifier of the object for which this feature map was computed.
                    - "featureMap" | An object containing the new feature map that was computed.
        Returns:
            None
        """
        object_id = message["objectId"]
        feature_map = message["featureMap"]

        try:
            objects[object_id].update_feature_map(feature_map)
        except KeyError:
            logger.log("Unknown object id")

        for processor in processors.values():
            processor.send_message(json.dumps({
                "type": "featureMap",
                "objectId": object_id,
                "featureMap": feature_map
            }))

    def send_mock_commands(self, message):
        """Sends a few mock messages to the processor for testing purposes

        Args:
            message (json):
                JSON message that was received. It should contain the following properties:
                    - "frameId"  | The identifier of a frame that should be used in the mock "start" command.
                    - "objectId" | The identifier of an object that should be used in the mock "start" command.
        Returns:
            None
        """
        frame_id = message["frameId"]
        box_id = message["boxId"]
        tracking_object1 = TrackingObject()

        tracking_object2 = TrackingObject()

        self.send_message(json.dumps({
            "type": "start",
            "objectId": tracking_object1.identifier,
            "frameId": frame_id,
            "boxId": box_id
        }))

        sleep(2)

        self.send_message(json.dumps({
            "type": "featureMap",
            "objectId": tracking_object2.identifier,
            "featureMap": {}
        }))

        sleep(2)

        self.send_message(json.dumps({
            "type": "stop",
            "objectId": tracking_object1.identifier
        }))
