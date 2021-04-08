"""Contains a dummy class that inherits from websocket client and adds a queue for received messages

"""

import json
from src.websocket_client import WebsocketClient


async def create_dummy_client(url, identifier=None):
    """
    Method used to create a dummy websocket client object
    Args:
        url: Websocket url to connect to
        id: Identifier of the websocket. If the websocket is not used as a processor socket,
        set id to None. Otherwise, set to an identifier.

    Returns: Websocket dummy client object
    """
    client = WebsocketClientDummy(url, identifier)
    await client.connect()
    return client


class WebsocketClientDummy(WebsocketClient):
    """Superclass of WebsocketClient to test receiving messages. Don't instantiate directly, call method
    create_dummy_client instead.

    """

    def __init__(self, url, identifier):

        super().__init__(url, identifier)
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
