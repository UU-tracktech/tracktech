"""Defines the websocket client class used for the unit tests.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.websocket.websocket_client import WebsocketClient


class DummyWebsocketClient(WebsocketClient):
    """Dummy websocket client that saves the last message.

    Attributes:
        last_message_type (str): Type of the last message.
        last_message (str): Content of the last message.
    """
    def __init__(self, websocket_url, identifier=None):
        """Initialized the dummy websocket, extending the properties.

        Args:
            websocket_url (str): URL of the WebSocket server.
            identifier (str): Identifier of the processor with which to connect.
        """
        super().__init__(websocket_url, identifier)
        self.last_message_type = None
        self.last_message = None

    def update_feature_map(self, message):
        """Override for the update_feature_map method that saves the message.

        Args:
            message (str): Feature map message gotten from the websocket to.
        """
        self.last_message_type = 'featureMap'
        self.last_message = message

    def start_tracking(self, message):
        """Override for the start_tracking method that saves the message.

        Args:
            message (str): Message gotten from WebSocket to start tracking.
        """
        self.last_message_type = 'start'
        self.last_message = message

    def stop_tracking(self, message):
        """Override for the stop_tracking method that saves the message.

        Args:
            message (str): Message gotten from the WebSocket to stop tracking.
        """
        self.last_message_type = 'stop'
        self.last_message = message
