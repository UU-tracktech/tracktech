"""Test the websocket client for what is possible with unit testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import tornado
import tornado.testing
import tornado.web
from tornado.websocket import WebSocketHandler

from tests.unittests.utils.echo_websocket_handler import EchoWebsocketHandler
from tests.unittests.utils.websocket_coroutines import WebsocketCoroutines
from tests.unittests.utils.dummy_websocket_client import DummyWebsocketClient


# pylint: disable=protected-access.
class TestWebsocketClient(WebsocketCoroutines):
    """Tests the websocket client using different coroutines to create a websocket connection.

    Attributes:
        start_message (str): Start message in json format.
        stop_message (str): Stop message in json format.
        feature_map_message (str): Feature map json message.
    """
    start_message = '{"type": "start", "objectId": 1, "frameId": 1, "boxId": 1}'
    stop_message = '{"type": "stop", "objectId": 1}'
    feature_map_message = '{"type": "featureMap", "objectId": 1, "featureMap": []}'

    def get_app(self):
        """Tornado testing creates the application and starts it in the background.

        Returns:
            tornado.web.Application: Web application containing two websocket handlers.
        """
        return tornado.web.Application([
            (r'/', WebSocketHandler),
            (r'/echo', EchoWebsocketHandler)
        ])

    def test_constructor(self):
        """Tests the constructor whether the url gets saved correctly."""
        ws_url = 'ws://localhost:80'
        dummy_websocket = DummyWebsocketClient(ws_url)
        assert dummy_websocket.websocket_url == ws_url

    @tornado.testing.gen_test(timeout=10)
    def test_connect(self):
        """Test whether websocket is able to connect without an identifier and checks properties."""
        dummy_websocket = yield self.dummy_ws_connect("/")
        assert dummy_websocket.connection is not None
        assert not dummy_websocket.reconnecting
        # Check whether connecting was successful.
        assert dummy_websocket.connection.protocol

    @tornado.testing.gen_test(timeout=10)
    def test_connect_with_identifier(self):
        """Test whether websocket is able to connect with an identifier and checks properties."""
        # Connect with the identifier.
        identifier = 'mock_id'
        dummy_websocket = yield self.dummy_ws_connect("/", identifier)

        assert dummy_websocket.identifier == identifier
        assert dummy_websocket.connection is not None
        assert not dummy_websocket.reconnecting

        # Check whether connecting was successful.
        assert dummy_websocket.connection.protocol
