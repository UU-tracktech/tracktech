"""Entry point of the application.

This file sets up the tornado application.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import asyncio
import os

from tornado.ioloop import IOLoop
from tornado.web import Application

from src.utility.get_auth import get_auth_params
from src.utility.http_server import create_http_servers
from src.objects.object_management import start_tracking_timeout_monitoring
from src.handlers.client_socket import ClientSocket
from src.handlers.processor_socket import ProcessorSocket
from src.handlers.timeline_handler import TimelineHandler
from src.handlers.object_ids_handler import ObjectIdsHandler


def main():
    """Entry point of the application.

    The main method is used to set up the tornado application, which includes routing, setting up
    SSL certificates and compiling the documentation.
    """
    # Get auth ready by reading the environment variables.
    (client_auth, processor_auth) = get_auth_params()

    app = create_app(client_auth, processor_auth)

    # Create http servers.
    create_http_servers(app)

    # Start a tracking timeout process if it is given.
    timeout = os.environ.get('TRACKING_TIMEOUT')
    if timeout is not None:
        start_tracking_timeout_monitoring(int(timeout), asyncio.get_event_loop())

    IOLoop.current().start()


def create_app(client_auth, processor_auth):
    """Creates tornado application.

    Creates the routing in the application and returns the complete app.

    Args:
        client_auth (Auth): An auth object to validate clients with.
        processor_auth (Auth): An auth object to validate processors with.

    Returns:
        Application: The tornado application with handlers
    """
    # Define socket for both client and processor.
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/timelines', TimelineHandler),
        ('/objectIds', ObjectIdsHandler)
    ]

    # Construct and serve the tornado application.
    return Application(handlers, client_auth=client_auth, processor_auth=processor_auth)


if __name__ == "__main__":
    main()
