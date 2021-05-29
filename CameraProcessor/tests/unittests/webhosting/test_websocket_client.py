"""Test the websocket client for what is possible with unit testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import asyncio
import tornado
import tornado.testing
import tornado.web
from tornado.websocket import WebSocketHandler

from processor.webhosting.websocket_client import WebsocketClient

from tests.unittests.webhosting.conftest import messages_are_equal
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
        # Connect with identifier.
        identifier = 'mock_id'
        dummy_websocket = yield self.dummy_ws_connect("/", identifier)

        assert dummy_websocket.identifier == identifier
        assert dummy_websocket.connection is not None
        assert not dummy_websocket.reconnecting

        # Check whether connecting was successful.
        assert dummy_websocket.connection.protocol

    @tornado.testing.gen_test(timeout=10)
    def test_write_message_after_disconnect(self):
        """Writes message after disconnecting."""
        dummy_websocket = yield self.dummy_ws_connect("/")
        dummy_websocket.connection = None
        yield dummy_websocket._write_message(self.feature_map_message)
        assert len(dummy_websocket.write_queue) == 1

    @tornado.testing.gen_test(timeout=10)
    def test_write_message_queue_away(self):
        """Fills up the message queue and checks whether a new write empties the queue."""
        # Fill up message queue.
        dummy_websocket = yield self.dummy_ws_connect("/")
        dummy_websocket.write_queue = [self.feature_map_message, self.stop_message, self.start_message]
        assert len(dummy_websocket.write_queue) == 3

        yield dummy_websocket._write_message(self.feature_map_message)

        # Wait until message queue is empty.
        while len(dummy_websocket.write_queue) != 0:
            yield asyncio.sleep(0)

    @tornado.testing.gen_test(timeout=10)
    def test_websocket_send_featuremap(self):
        """Send a featuremap in echo handler and checks whether correct handler is used."""
        # Connect and write.
        dummy_websocket = DummyWebsocketClient('')
        dummy_websocket_connection = yield self.ws_connect('/echo', on_message_callback=dummy_websocket._on_message)
        yield dummy_websocket_connection.write_message(self.feature_map_message)

        # Wait for the message to be received.
        while dummy_websocket.last_message is None:
            yield asyncio.sleep(0)

        # Assert the json is received by the correct handler.
        assert dummy_websocket.last_message_type == 'featureMap'
        assert messages_are_equal(self.feature_map_message, dummy_websocket.last_message)

    @tornado.testing.gen_test(timeout=10)
    def test_websocket_send_start(self):
        """Send a start command in echo handler and checks whether correct handler is used."""
        # Connect and write.
        dummy_websocket = DummyWebsocketClient('')
        dummy_websocket_connection = yield self.ws_connect('/echo', on_message_callback=dummy_websocket._on_message)
        yield dummy_websocket_connection.write_message(self.start_message)

        # Wait for the message to be received.
        while dummy_websocket.last_message is None:
            yield asyncio.sleep(0)

        # Assert the json is received by the correct handler.
        assert dummy_websocket.last_message_type == 'start'
        assert messages_are_equal(self.start_message, dummy_websocket.last_message)

    @tornado.testing.gen_test(timeout=10)
    def test_websocket_send_stop(self):
        """Send a stop command in echo handler and checks whether correct handler is used."""
        # Connect and write.
        dummy_websocket = DummyWebsocketClient('')
        dummy_websocket_connection = yield self.ws_connect('/echo', on_message_callback=dummy_websocket._on_message)
        yield dummy_websocket_connection.write_message(self.stop_message)

        # Wait for the message to be received.
        while dummy_websocket.last_message is None:
            yield asyncio.sleep(0)

        # Assert the json is received by the correct handler.
        assert dummy_websocket.last_message_type == 'stop'
        assert messages_are_equal(self.stop_message, dummy_websocket.last_message)

    def test_empty_message(self):
        """Tests whether empty message is handled correctly."""
        dummy_websocket = DummyWebsocketClient('')
        dummy_websocket._on_message('')

    def test_receive_featuremap(self):
        """Tests receiving a featuremap."""
        websocket = WebsocketClient('')
        websocket._on_message(self.feature_map_message)

    def test_start_tracking(self):
        """Tests start tracking command."""
        websocket = WebsocketClient('')
        websocket._on_message(self.start_message)

    def test_stop_tracking(self):
        """Tests stop tracking command."""
        websocket = WebsocketClient('')
        websocket._on_message(self.stop_message)

    def test_wrong_type(self):
        """Wrong type gets handled correctly."""
        dummy_websocket = DummyWebsocketClient('')
        dummy_websocket._on_message('{"type": "yes"}')
