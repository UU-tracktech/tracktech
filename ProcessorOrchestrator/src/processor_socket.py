"""Processor component to handle processor websocket connections.

This file contains a websocket class to handle websocket connections coming from camera processors. It defines multiple
functions that can be called using specified json messages.
"""

import json
from typing import Optional, Awaitable, Dict, Callable, Any
import tornado.web
from time import sleep
from tornado import httputil
from tornado.websocket import WebSocketHandler
from object_manager import objects, TrackingObject
from connections import processors
import client_socket
import logger


class ProcessorSocket(WebSocketHandler):
    """Websocket handler for camera processors.

    Attributes:
        identifier: An int that serves as the unique identifier to this object.
    """

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest):
        """Creates unique id and appends it to the dict of processors.

        Args:
            application: The tornado web application
            request: The HTTP server request
        """
        super().__init__(application, request)
        self.identifier = max(processors.keys(), default=0) + 1

    def check_origin(self, origin: str) -> bool:
        """Override to enable support for allowing alternate origins.

        Args:
            origin:
                Origin of the HTTP request, is ignored as all origins are allowed.
        """
        return True

    def open(self) -> None:
        """Called upon opening of the websocket.

        Method called upon the opening of the websocket. After connecting, it appends this component to a dict
        of other websockets.
        """
        logger.log_connect("/processor", self.request.remote_ip)
        print(f"New processor connected with id: {self.identifier}")
        processors[self.identifier] = self

    def on_message(self, message: str) -> None:
        """Handles a message from a processor that is received on the websocket.

        Method which handles messages coming in from a processor. The messages are expected in json format.

        Args:
            message:
                JSON with at least a "type" property. This property can have the following values:
                    - "boundingBoxes" | This signifies a message that contains bounding boxes, see send_bounding_boxes
                                        for the other expected properties.
                    - "featureMap"    | This signifies a message that contains a feature map of an object,
                                        see update_feature_map, for the other expected properties.
                    - "test"          | This values will be answered with a series of messages mocking the messages
                                        a processor might expect, see send_mock_commands for the other expected
                                        properties.
        """
        logger.log_message_receive(message, "/processor", self.request.remote_ip)

        try:
            message_object: json = json.loads(message)

            # Switch on message type
            actions: Dict[str, Callable[[], None]] = {
                "boundingBoxes":
                    lambda: self.send_bounding_boxes(message_object),
                "featureMap":
                    lambda: self.update_feature_map(message_object),
                "test":
                    lambda: self.send_mock_commands(message_object)
            }

            # Execute correct function
            function = actions.get(message_object["type"])
            """type: Optional[Callable[[], None]]"""

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

    def send_message(self, message) -> None:
        """Sends a message over the websocket and logs it.

        Args:
            message: string which should be send over this websocket
        """
        logger.log_message_send(message, "/processor", self.request.remote_ip)
        self.write_message(message)

    def on_close(self) -> None:
        """Called when the websocket is closed, deletes itself from the dict of processors."""
        logger.log_disconnect("/processor", self.request.remote_ip)
        del processors[self.identifier]
        print(f"Processor with id {self.identifier} disconnected")

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """Unused method that could handle streamed request data"""
        pass

    def send_bounding_boxes(self, message) -> None:
        """Sends bounding boxes to all clients

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "frameId" | The identifier of the frame for which these bounding boxes were computed.
                    - "boxes"   | An object containing the bounding boxes that were computed for this frame.
        """
        frame_id: Any = message["frameId"]
        boxes: json = message["boxes"]

        if len(client_socket.clients.values()) > 0:
            for c in client_socket.clients.values():
                c.send_message(json.dumps({
                    "type": "boundingBoxes",
                    "cameraId": self.identifier,
                    "frameId": frame_id,
                    "boxes": boxes
                }))

    @staticmethod
    def update_feature_map(message) -> None:
        """Sends an updated feature map to all processors

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "objectId"   | The identifier of the object for which this feature map was computed.
                    - "featureMap" | An object containing the new feature map that was computed.
        """
        object_id: int = message["objectId"]
        feature_map: json = message["featureMap"]

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

    def send_mock_commands(self, message) -> None:
        """Sends a few mock messages to the processor for testing purposes

        Args:
            message:
                JSON message that was received. It should contain the following properties:
                    - "frameId"  | The identifier of a frame that should be used in the mock "start" command.
                    - "objectId" | The identifier of an object that should be used in the mock "start" command.
        """
        frame_id: Any = message["frameId"]
        box_id: int = message["boxId"]
        tracking_object1: TrackingObject = TrackingObject()

        tracking_object2: TrackingObject = TrackingObject()

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
