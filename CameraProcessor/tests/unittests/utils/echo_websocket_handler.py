"""Defines the echo websocket handler that is used for the unit tests

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import asyncio
import tornado.gen
from tornado.websocket import WebSocketHandler, WebSocketClosedError
# from tests.unittests.utils.websocket_handler import GenericWebsocketHandler


class EchoWebsocketHandler(WebSocketHandler):
    """A websocket handler that echos the message back to the client

    """
    @tornado.gen.coroutine
    def on_message(self, message):
        """Overrides the on_message and echos the message back

        Args:
            message (str): string message the websocket handler receives
        """
        try:
            yield self.write_message(message, isinstance(message, bytes))
        except asyncio.CancelledError:
            pass
        except WebSocketClosedError:
            pass
