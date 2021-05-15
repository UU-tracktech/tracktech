"""Coroutines for the test_websocket_client.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest
import tornado.web
import tornado.gen
from tornado.websocket import websocket_connect
from tornado.testing import AsyncHTTPTestCase

from tests.unittests.utils.dummy_websocket_client import DummyWebsocketClient


class WebsocketCoroutines(AsyncHTTPTestCase):
    """Create websocket coroutines that connect to a handler

    """
    @pytest.mark.asyncio
    async def dummy_ws_connect(self, path, identifier=None):
        """Asynchronous way to connect the dummy websocket to a given url

        Args:
            path (str): The path to which the websocket connects
            identifier (str): The identifier given t

        Returns:
            DummyWebsocketClient: A dummy websocket client used for testing
        """
        ws_url = "ws://127.0.0.1:%d%s" % (self.get_http_port(), path)
        dummy_websocket = DummyWebsocketClient(ws_url, identifier)
        # Connect websocket
        await dummy_websocket.connect()
        return dummy_websocket

    @tornado.gen.coroutine
    def ws_connect(self, path, **kwargs):
        """Connect the websocket to a given path

        Args:
            path (str): Path to the websocket handler
            **kwargs: Contains any other argument that be given to the connection

        Returns:
            websocket.Connection: Websocket connection that is created by the coroutine
        """
        ws = yield websocket_connect(
            "ws://127.0.0.1:%d%s" % (self.get_http_port(), path), **kwargs
        )
        raise tornado.gen.Return(ws)
