from src.websocket_client import WebsocketClient
import json


class WebsocketClientDummy(WebsocketClient):
    """Superclass of WebsocketClient to test receiving messages

    """

    def __init__(self, url):

        super().__init__(url)
        self.message_list = []

    def on_message(self, message):
        """
        On message callback function

        Args:
            message: the raw message posted on the websocket
        """

        # Websocket closed, reconnect is handled by write_message
        if message:
            message_json = json.loads(message)
            self.message_list.append(message_json)

    async def await_message(self, length):
        """Waits for message list to be filled.

        Args:
            length: expected length of message_list

        Returns:

        """
        while len(self.message_list) < length:
            continue
        return
