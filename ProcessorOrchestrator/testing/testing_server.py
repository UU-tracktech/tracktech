"""Server used for testing purposes. It is run as a test so that coverage may be measured."""

import pytest
import tornado
from tornado import httputil
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from src.client_socket import ClientSocket
from src.processor_socket import ProcessorSocket
from src.log_handler import LogHandler


@pytest.mark.asyncio
def test_start_testing_server():
    """Starts the server as a test, so that the coverage may be measured."""
    main()


def main():
    """Starts the server."""
    print("Starting main")

    _start_server()


def _start_server():
    """Creates handlers and starts the IO loop."""
    print("Starting setup server")

    server_container = []

    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler),
        ('/stop', StopSocket, dict(server=server_container))
    ]

    app = Application(handlers)
    server = HTTPServer(app)
    server_container.append(server)
    server.listen(80)
    print("Test server is listening")
    IOLoop.current().start()


def stop_server(server):
    """Stops the server."""

    server.stop()
    io_loop = IOLoop.instance()
    io_loop.add_callback(io_loop.stop)


class StopSocket(WebSocketHandler):
    """Websocket handler that can only be used to stop the server."""

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest):
        """Initialises testing server."""
        super().__init__(application, request)
        self.server = None

    def initialize(self, server):
        """Sets server."""
        self.server = server

    def data_received(self, chunk):
        """Override to handle received data, unused."""

    def check_origin(self, origin: str) -> bool:
        """Override to enable support for allowing alternate origins.

        Args:
            origin:
                Origin of the HTTP request, is ignored as all origins are allowed.
        """
        return True

    def on_message(self, message) -> None:
        """Waits for test message

        Args:
            message:
                String that should contain the string 'stop', which will stop the server.
        """
        if message == "stop":
            stop_server(self.server[0])
