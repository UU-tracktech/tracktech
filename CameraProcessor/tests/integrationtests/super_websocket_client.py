import asyncio
import os
from src.websocket_client import WebsocketClient
import json
import pytest
import tornado
import tornado.testing
import tornado.gen
from tornado import websocket
import tornado.web
from utils.jsonloader import load_data
from async_timeout import timeout


class WebsocketClientDummy(WebsocketClient):

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
        while len(self.message_list) < length:
            continue
        return
