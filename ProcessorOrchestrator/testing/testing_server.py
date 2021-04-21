import threading
import time
import sys
import os

import pytest
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

# pytest resolves this reference internally
# noinspection PyUnresolvedReferences
from src.client_socket import ClientSocket
# noinspection PyUnresolvedReferences
from src.processor_socket import ProcessorSocket
# noinspection PyUnresolvedReferences
from src.log_handler import LogHandler
from tornado.websocket import WebSocketHandler

global thread
global server
global stop

@pytest.mark.asyncio
@pytest.mark.timeout(20000)
def test_start_testing_server():
    global stop
    stop = False

    main()

    assert stop


def main():
    print("Starting main")

    _setup_server()

    global stop
    global thread

    while not stop:
        time.sleep(1)

    _stop_server()
    thread.join()


def _setup_server():
    global thread

    print("Starting setup server")
    thread = threading.Thread(target=_start_server)
    # thread.daemon = True
    thread.start()


def _start_server():
    global server
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler),
        ('/stop', StopSocket)
    ]

    app = Application(handlers)
    server = HTTPServer(app)
    server.listen(80)
    print("Test server is listening")
    IOLoop.current().start()


def _stop_server():
    global server

    server.stop()
    io_loop = IOLoop.instance()
    io_loop.add_callback(io_loop.stop)


class StopSocket(WebSocketHandler):
    def data_received(self, chunk):
        pass

    def check_origin(self, origin: str) -> bool:
        """Override to enable support for allowing alternate origins.

        Args:
            origin:
                Origin of the HTTP request, is ignored as all origins are allowed.
        """
        return True

    def on_message(self, message) -> None:
        global stop
        """Waits for test message"""
        if message == "stop":
            stop = True
