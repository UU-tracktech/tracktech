"""Test the websocket client for what is possible with unit testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import asyncio
import pytest
import tornado
import tornado.testing
import tornado.web
from tornado.httpclient import HTTPClientError
from tornado.websocket import WebSocketHandler

from tests.unittests.utils.echo_websocket_handler import EchoWebsocketHandler
from tests.unittests.utils.websocket_coroutines import WebsocketCoroutines
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.websocket.websocket_client import WebsocketClient
from processor.websocket.boxes_message import BoxesMessage
from processor.websocket.start_message import StartMessage
from processor.websocket.stop_message import StopMessage
from processor.websocket.update_message import UpdateMessage


# pylint: disable=protected-access.
class TestWebsocketClient(WebsocketCoroutines):
    """Tests the websocket client using different coroutines to create a websocket connection.

    Attributes:
        start_message (StartMessage): Start message in json format.
        stop_message (StopMessage): Stop message in json format.
        feature_map_message (UpdateMessage): Feature map json message.
    """
    start_message = StartMessage.from_message({'type': 'start', 'objectId': 1, 'frameId': 1.0, 'boxId': 1})
    stop_message = StopMessage.from_message({'type': 'stop', 'objectId': 1})
    feature_map_message = UpdateMessage.from_message({'objectId': 1, 'featureMap': [1.1]})
    boxes_message = BoxesMessage(1., BoundingBoxes([]))

    def get_app(self):
        """Tornado testing creates the application and starts it in the background.

        Returns:
            tornado.web.Application: Web application containing two websocket handlers.
        """
        return tornado.web.Application([
            (r'/', WebSocketHandler),
            (r'/echo', EchoWebsocketHandler)
        ])

    def test_init(self):
        """Tests the constructor whether the url gets saved correctly."""
        ws_url = 'ws://localhost:80'
        identifier = 'test stream 1'
        dummy_websocket = WebsocketClient(ws_url, identifier)
        assert dummy_websocket.websocket_url == ws_url
        assert dummy_websocket.identifier == identifier

    @tornado.testing.gen_test(timeout=10)
    def test_connect(self):
        """Test whether websocket is able to connect without an identifier and checks properties."""
        dummy_websocket = yield self.dummy_ws_connect('/')
        assert dummy_websocket.connection is not None
        assert not dummy_websocket.reconnecting
        # Check whether connecting was successful.
        assert dummy_websocket.connection.protocol

    @tornado.testing.gen_test(timeout=10)
    def test_reconnect(self):
        """Writes message after disconnecting."""
        dummy_websocket = yield self.dummy_ws_connect('/')
        dummy_websocket.connection = None
        dummy_websocket.reconnecting = False
        dummy_websocket.send_message(self.feature_map_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(0)

        # Connection object is regenerated and message is inside the write_queue.
        assert len(dummy_websocket.write_queue) == 0

    @tornado.testing.gen_test(timeout=10)
    def test_connect_invalid_extension(self):
        """Test handling wrong websocket url."""
        with pytest.raises(HTTPClientError):
            yield self.dummy_ws_connect('/invalid')

    @tornado.testing.gen_test(timeout=10)
    def test_connect_with_identifier(self):
        """Test whether websocket is able to connect with an identifier and checks properties."""
        # Connect with the identifier.
        identifier = 'mock_id'
        dummy_websocket = yield self.dummy_ws_connect('/', identifier)

        assert dummy_websocket.identifier == identifier
        assert dummy_websocket.connection is not None
        assert not dummy_websocket.reconnecting

        # Check whether connecting was successful.
        assert dummy_websocket.connection.protocol

    @tornado.testing.gen_test(timeout=40)
    def test_write_message_after_disconnect(self):
        """Writes a message after disconnecting."""
        dummy_websocket = yield self.dummy_ws_connect('/', 'mock_id')
        dummy_websocket.connection = None
        dummy_websocket.reconnecting = True
        dummy_websocket.send_message(self.feature_map_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(0)

        # Message was still appended to the write queue.
        assert len(dummy_websocket.write_queue) == 1

    @tornado.testing.gen_test(timeout=10)
    def test_write_message(self):
        """Writes message after disconnecting."""
        dummy_websocket = yield self.dummy_ws_connect('/', 'mock_id')
        dummy_websocket.send_message(self.feature_map_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(0)
        assert len(dummy_websocket.write_queue) == 0

    @tornado.testing.gen_test(timeout=10)
    def test_receive_update_message(self):
        """Writes update message to echo websocket and check that it is received correctly."""
        dummy_websocket = yield self.dummy_ws_connect('/echo', 'mock_id')
        dummy_websocket.send_message(self.feature_map_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(4)

        assert dummy_websocket.message_queue.popleft() == self.feature_map_message

    @tornado.testing.gen_test(timeout=10)
    def test_receive_start_message(self):
        """Writes start message to echo websocket and check that it is received correctly."""
        dummy_websocket = yield self.dummy_ws_connect('/echo', 'mock_id')
        dummy_websocket.send_message(self.start_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(4)

        assert dummy_websocket.message_queue.popleft() == self.start_message

    @tornado.testing.gen_test(timeout=10)
    def test_receive_stop_message(self):
        """Writes start message to echo websocket and check that it is received correctly."""
        dummy_websocket = yield self.dummy_ws_connect('/echo', 'mock_id')
        dummy_websocket.send_message(self.stop_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(4)

        assert dummy_websocket.message_queue.popleft() == self.start_message

    @tornado.testing.gen_test(timeout=10)
    def test_dont_receive_boxes_message(self):
        """Writes start message to echo websocket and check that it is not added to message queue.

        BoxesMessage is explicitly not handled by the websocket, since the processor does not expect to receive it.
        """
        dummy_websocket = yield self.dummy_ws_connect('/echo', 'mock_id')
        dummy_websocket.send_message(self.boxes_message)

        # Give the event loop the control to send the message.
        yield asyncio.sleep(4)

        assert len(dummy_websocket.message_queue) == 0
