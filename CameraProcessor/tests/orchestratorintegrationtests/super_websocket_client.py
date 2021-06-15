"""Contains a dummy class that inherits from websocket client and adds a queue for received messages.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json
from processor.websocket.websocket_client import WebsocketClient


async def create_dummy_client(url, identifier=None):
    """Method used to create a dummy websocket client object.

    Args:
        url (str): Websocket url to connect to
        identifier (str): Identifier of the websocket. If the websocket is not used as a processor socket,
                          set id to None. Otherwise, set to an identifier.

    Returns:
        WebsocketClientDummy: Websocket dummy client object.
    """
    client = WebsocketClientDummy(url, identifier)
    await client.connect()
    return client


class WebsocketClientDummy(WebsocketClient):
    """Superclass of WebsocketClient to test receiving messages.

    Note:
        Don't instantiate directly, call method create_dummy_client instead.
    """

    def __init__(self, url, identifier):
        """Initialises a websocket for testing purposes.

        Args:
            url (str): Websocket url to connect to.
            identifier (str): Identifier of the current processor.
        """
        super().__init__(url, identifier)
        self.message_list = []

    def on_message(self, message):
        """On message callback function.

        Overrides in order to add logic where the message is remembered.

        Args:
            message (Union[str, bytes]): the raw message posted on the websocket.
        """

        # Websocket closed, reconnect is handled by write_message.
        if message:
            message_json = json.loads(message)
            self.message_list.append(message_json)

    async def await_message(self, length):
        """Waits for message list to be filled.

        Args:
            length (int): expected length of message_list.
        """
        while len(self.message_list) < length:
            continue
        return
