"""Coroutines for the test_websocket_client.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from tornado.websocket import WebSocketHandler


class GenericWebsocketHandler(WebSocketHandler):
    """Base class for testing handlers that exposes the on_close event.
    This allows for tests to see the close code and reason on the
    server side.
    """
    def initialize(self, close_future=None, compression_options=None):
        self.close_future = close_future
        self.compression_options = compression_options

    def get_compression_options(self):
        return self.compression_options

    def on_close(self):
        if self.close_future is not None:
            self.close_future.set_result((self.close_code, self.close_reason))
