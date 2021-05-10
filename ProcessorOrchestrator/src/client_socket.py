"""Client component to handle client websocket connections.

This file contains a websocket class to handle websocket connections coming from clients (using the interface).
It defines multiple functions that can be called using specified json messages.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json
from time import sleep

from tornado.websocket import WebSocketHandler

from src.object_manager import TrackingObject, objects
from src.connections import processors, clients
import src.logger as logger


class ClientSocket(WebSocketHandler):
    """Websocket handler for camera processors.

    Attributes:
        identifier: An int that serves as the unique identifier to this object.
        authorized: A bool that shows whether the websocket connection is authorized.
    """

    def __init__(self, application, request):
        """Creates unique id and appends it to the dict of clients.

        Args:
            application (tornado.web.Application): The tornado web application
            request (httputil.HTTPServerRequest): The HTTP server request
        """
        super().__init__(application, request)
        self.identifier = max(clients.keys(), default=0) + 1
        self.authorized = False

        # Load the auth object from appsettings
        self.auth = self.application.settings.get('client_auth')

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

        Method called upon the opening of the websocket. After connecting, it appends this component
        to a dict of other websockets.

        Returns:
            None
        """
        logger.log_connect("/client", self.request.remote_ip)
        logger.log(f"New client connected with id: {self.identifier}")
        clients[self.identifier] = self

    # pylint: disable=broad-except
    def on_message(self, message):
        """Handles a message from a client that is received on the websocket.

        Method which handles messages coming in from a client. The messages are expected in json
        format.

        Args:
            message (string):
                JSON with at least a "type" property. This property can have the following values:
                    - "start" | This command is used to start the tracking of an object in the specified frame,
                                see start_tracking, for the other expected properties.
                    - "stop"  | This command is used to stop the tracking of an object,
                                see stop_tracking, for the other expected properties.
                    - "test"  | This values will be answered with a series of messages mocking the messages
                                a client might expect, see send_mock_data for the other expected properties.
        Returns:
            None
        """
        logger.log_message_receive(message, "/client", self.request.remote_ip)

        try:
            message_object = json.loads(message)

            # Switch on message type
            actions = {
                "start":
                    lambda: self.start_tracking(message_object),
                "stop":
                    lambda: self.stop_tracking(message_object)
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
                logger.log("A client was not authenticated first")

        except ValueError as exc:
            logger.log_error("/client", "ValueError", self.request.remote_ip)
            print("Someone wrote bad json", exc)
        except KeyError as exc:
            logger.log_error("/client", "KeyError", self.request.remote_ip)
            print("Someone missed a property in their json", exc)
        except Exception as exc:
            print(exc)
            logger.log("Someone wrote bad json")

    def send_message(self, message):
        """Sends a message over the websocket and logs it.

        Args:
            message (string): string which should be send over this websocket
        Returns:
            None
        """
        logger.log_message_send(message, "/client", self.request.remote_ip)
        self.write_message(message)

    def data_received(self, chunk):
        """Unused method that could handle streamed request data"""

    def on_close(self):
        """Called when the websocket is closed, deletes itself from the dict of clients.

        Returns:
            None
        """
        logger.log_disconnect("/client", self.request.remote_ip)
        del clients[self.identifier]
        logger.log(f"Client with id {self.identifier} disconnected")

    def authenticate(self, message):
        """Authenticates a client

        Args:
            message(json):
                JSON message that was received. It should contain the following property:
                    - "jwt" | The jwt token containing information about a user
        """

        if self.auth is not None:
            self.auth.validate(message["jwt"])
            self.authorized = True

    @staticmethod
    def start_tracking(message):
        """Creates tracking object and sends start tracking command to specified processor

        Args:
            message (json):
                JSON message that was received. It should contain the following properties:
                    - "cameraId" | The identifier of the processor on which the bounding box of the object to be tracked
                                   was computed.
                    - "frameId"  | The identifier of the frame on which the bounding box of the object to be tracked
                                   was computed.
                    - "boxId"    | The identifier of the bounding box computed for the object to be tracked.
        Returns:
            None
        """
        camera_id = message["cameraId"]
        frame_id = message["frameId"]
        box_id = message["boxId"]

        if camera_id not in processors.keys():
            logger.log("Unknown processor")
            return

        tracking_object = TrackingObject()

        logger.log(
            f"New tracking object created with id {tracking_object.identifier}, "
            f"found at bounding box with Id {box_id} on frame {frame_id} of camera {camera_id}")

        processors[camera_id].send_message(json.dumps({
            "type": "start",
            "objectId": tracking_object.identifier,
            "frameId": frame_id,
            "boxId": box_id
        }))

    @staticmethod
    def stop_tracking(message):
        """Removes tracking object and sends stop tracking command to all processors

        Args:
            message (json):
                JSON message that was received. It should contain the following properties:
                    - "objectId" | The identifier of the object which should no longer be tracked.
        """
        object_id = message["objectId"]
        if object_id not in objects.keys():
            logger.log("unknown object")
            return

        objects[object_id][0].remove_self()

        if len(processors) > 0:
            for processor in processors.values():
                processor.send_message(json.dumps({
                    "type": "stop",
                    "objectId": object_id
                }))

        logger.log(f"stopped tracking of object with id {object_id}")
