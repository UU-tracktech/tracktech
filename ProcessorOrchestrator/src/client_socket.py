"""Client component to handle client websocket connections.

This file contains a websocket class to handle websocket connections coming from clients (using the interface).
It defines multiple functions that can be called using specified json messages.
"""

import json
from time import sleep
from typing import Optional, Awaitable, Dict, Callable, Any

import tornado.web
from tornado import httputil
from tornado.websocket import WebSocketHandler

from src.object_manager import TrackingObject, objects
from src.connections import processors, clients
import logger


class ClientSocket(WebSocketHandler):
    """Websocket handler for camera processors.

    Attributes:
        identifier: An int that serves as the unique identifier to this object.
    """

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest):
        """Creates unique id and appends it to the dict of clients.

        Args:
            application: The tornado web application
            request: The HTTP server request
        """
        super().__init__(application, request)
        self.identifier = max(clients.keys(), default=0) + 1

    def check_origin(self, origin) -> bool:
        """Override to enable support for allowing alternate origins.

        Args:
            origin:
                Origin of the HTTP request, is ignored as all origins are allowed.
        """
        return True

    def open(self, _pattern) -> None:
        """Called upon opening of the websocket.

        Method called upon the opening of the websocket. After connecting, it appends this component
        to a dict of other websockets.
        """
        logger.log_connect("/client", self.request.remote_ip)
        print(f"New client connected with id: {self.identifier}")
        clients[self.identifier] = self

    def on_message(self, message) -> None:
        """Handles a message from a client that is received on the websocket.

        Method which handles messages coming in from a client. The messages are expected in json
        format.

        Args:
            message:
                JSON with at least a "type" property. This property can have the following values:
                    - "start" | This command is used to start the tracking of an object in the specified frame,
                                see start_tracking, for the other expected properties.
                    - "stop"  | This command is used to stop the tracking of an object,
                                see stop_tracking, for the other expected properties.
                    - "test"  | This values will be answered with a series of messages mocking the messages
                                a client might expect, see send_mock_data for the other expected properties.
        """
        logger.log_message_receive(message, "/client", self.request.remote_ip)

        try:
            message_object: json = json.loads(message)

            # Switch on message type
            actions: Dict[str, Callable[[], None]] = {
                "start":
                    lambda: self.start_tracking(message_object),
                "stop":
                    lambda: self.stop_tracking(message_object),
                "test":
                    lambda: self.send_mock_data(message_object)
            }

            # Execute correct function
            function: Optional[Callable[[], None]] = actions.get(message_object["type"])
            if function is None:
                print("Someone gave an unknown command")
            else:
                function()

        except ValueError:
            logger.log_error("/client", "ValueError", self.request.remote_ip)
            print("Someone wrote bad json")
        except KeyError:
            logger.log_error("/client", "KeyError", self.request.remote_ip)
            print("Someone missed a property in their json")

    def send_message(self, message) -> None:
        """Sends a message over the websocket and logs it.

        Args:
            message: string which should be send over this websocket
        """
        logger.log_message_send(message, "/client", self.request.remote_ip)
        self.write_message(message)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """Unused method that could handle streamed request data"""

    def on_close(self) -> None:
        """Called when the websocket is closed, deletes itself from the dict of clients."""
        logger.log_disconnect("/client", self.request.remote_ip)
        del clients[self.identifier]
        print(f"Client with id {self.identifier} disconnected")

    @staticmethod
    def start_tracking(message) -> None:
        """Creates tracking object and sends start tracking command to specified processor

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "cameraId" | The identifier of the processor on which the bounding box of the object to be tracked
                                   was computed.
                    - "frameId"  | The identifier of the frame on which the bounding box of the object to be tracked
                                   was computed.
                    - "boxId"    | The identifier of the bounding box computed for the object to be tracked.
        """
        camera_id: Any = message["cameraId"]
        frame_id: Any = message["frameId"]
        box_id: int = message["boxId"]

        if camera_id not in processors.keys():
            print("Unknown processor")
            return

        tracking_object: TrackingObject = TrackingObject()

        print(
            f"New tracking object created with id {tracking_object.identifier}, "
            f"found at bounding box with Id {box_id} on frame {frame_id} of camera {camera_id}")

        processors[camera_id].send_message(json.dumps({
            "type": "start",
            "objectId": tracking_object.identifier,
            "frameId": frame_id,
            "boxId": box_id
        }))

    @staticmethod
    def stop_tracking(message) -> None:
        """Removes tracking object and sends stop tracking command to all processors

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "objectId" | The identifier of the object which should no longer be tracked.
        """
        object_id: int = message["objectId"]
        if object_id not in objects.keys():
            print("unknown object")
            return

        objects[object_id].remove_self()

        if len(processors) > 0:
            for processor in processors.values():
                processor.send_message(json.dumps({
                    "type": "stop",
                    "objectId": object_id
                }))

        print(f"stopped tracking of object with id {object_id}")

    def send_mock_data(self, message) -> None:
        """Sends a few mock messages to the client for testing purposes

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "cameraId"  | The identifier of a processor that should be used in the mock "start" command.
        """
        camera_id: Any = message["cameraId"]

        frame_id = 0

        for _ in range(50):
            self.send_message(json.dumps({
                "type": "boundingBoxes",
                "cameraId": camera_id,
                "frameId": frame_id,
                "boxes": {}
            }))

            frame_id += 1
            sleep(0.2)
