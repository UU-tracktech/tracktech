"""Server used for testing purposes. It is run as a test so that coverage may be measured.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import asyncio

import pytest
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from src.utility.http_server import create_http_servers
from src.handlers.client_socket import ClientSocket
from src.handlers.processor_socket import ProcessorSocket
from src.handlers.timeline_handler import TimeLineHandler
from src.objects.object_management import start_tracking_timeout_monitoring
from src.handlers.object_ids_handler import ObjectIdsHandler


@pytest.mark.asyncio
def test_start_testing_server():
    """Starts the server as a test, so that the coverage may be measured."""
    _start_server()


def _start_server():
    """Creates handlers and starts the IO loop."""
    print("Starting setup server")

    server_container = []

    # Create the handlers.
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/timelines', TimeLineHandler),
        ('/objectIds', ObjectIdsHandler),
        ('/stop', StopSocket, {'server': server_container})
    ]

    # Create the server application.
    app = Application(handlers)
    server, _ = create_http_servers(app)
    server_container.append(server)

    # Start the server.
    start_tracking_timeout_monitoring(10, asyncio.get_event_loop())
    IOLoop.current().start()


def stop_server(server):
    """Stops the server.

    Args:
        server (HTTPServer): Server the of the test that should be stopped
    """

    server.stop()
    io_loop = IOLoop.instance()
    io_loop.add_callback(io_loop.stop)


class StopSocket(WebSocketHandler):
    """Websocket handler that can only be used to stop the server.

    Attributes:
        server (HTTPServer): Server on which the test is ran.
    """

    def initialize(self, server):
        """Sets server.

        Args:
            server (HTTPServer): Server on which the test is ran.
        """
        # Noinspection PyAttributeOutsideInit | In tornado, the init function should be replaced with initialize.
        # pylint: disable=attribute-defined-outside-init
        self.server = server

    def data_received(self, chunk):
        """Override to handle received data, unused.

        Args:
            chunk (bytes): Byte data received from the server.
        """

    def check_origin(self, origin):
        """Override to enable support for allowing alternate origins.

        Args:
            origin (string): Origin of the HTTP request, is ignored as all origins are allowed.

        Returns:
            bool: Whether the origin is correct.
        """
        return True

    def on_message(self, message):
        """Waits for test message.

        Args:
            message (string): String that should contain the string 'stop', which will stop the server.
        """
        if message == "stop":
            stop_server(self.server[0])
