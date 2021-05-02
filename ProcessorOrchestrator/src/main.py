"""Entry point of the application

This file sets up the tornado application.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import ssl

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from auth.auth import Auth
from src.client_socket import ClientSocket
from src.processor_socket import ProcessorSocket
from src.log_handler import LogHandler
import src.logger as logger


def main():
    """Entry point of the application

    The main method is used to set up the tornado application, which includes routing, setting up
    SSL certificates and compiling the documentation.
    """
    # Get ssl ready, if provided in the environment variables
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None

    # Get auth ready by reading the environment variables
    public_key, audience = os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE')
    client_auth, processor_auth = None, None
    if public_key is not None and audience is not None:
        client_role = os.environ.get('CLIENT_ROLE')
        if client_role is not None:
            logger.log("using client token validation")
            client_auth = Auth(public_key_path=public_key, algorithms=['RS256'],
                audience=audience, role=client_role)
        processor_role = os.environ.get('PROCESSOR_ROLE')
        if processor_role is not None:
            logger.log("using processor token validation")
            processor_auth = Auth(public_key_path=public_key, algorithms=['RS256'],
                audience=audience, role=processor_role)

    app = create_app(client_auth, processor_auth)

    if use_tls:
        # Create a ssl context
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Create a http server, with optional ssl.
        https_server = HTTPServer(app, ssl_options=ssl_ctx)
        https_server.listen(443)
        logger.log('listening over https')

    # Create a http server, with optional ssl.
    http_server = HTTPServer(app)
    http_server.listen(80)
    logger.log('listening over http')

    IOLoop.current().start()


def create_app(client_auth, processor_auth):
    """Creates tornado application.

    Creates the routing in the application and returns the complete app.

    Args:
        client_auth:  A auth object to validate clients with
        processor_auth:  A auth object to validate processors with

    Returns:
        Application
    """
    # Define socket for both client and processor
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler)
    ]

    # Construct and serve the tornado application.
    return Application(handlers, client_auth=client_auth, processor_auth=processor_auth)


if __name__ == "__main__":
    main()
