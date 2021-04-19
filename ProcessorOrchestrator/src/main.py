"""Entry point of the application

This file sets up the tornado application.
"""
import os
import ssl

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from client_socket import ClientSocket
from processor_socket import ProcessorSocket
from log_handler import LogHandler


def main():
    """Entry point of the application

    The main method is used to set up the tornado application, which includes routing, setting up
    SSL certificates and compiling the documentation.
    """
    # Get ssl ready, if provided in the environment variables
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None

    app = create_app()

    # if use_tls:
    #     # Create a ssl context
    #     ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #     ssl_ctx.load_cert_chain(cert, key)
    #
    #     # Create a http server, with optional ssl.
    #     http_server = HTTPServer(app, ssl_options=ssl_ctx)
    #     http_server.listen(443)
    #     print('listening over https')
    #
    # else:
    # Create a http server, with optional ssl.
    http_server = HTTPServer(app)
    http_server.listen(80)
    print('listening over http')

    IOLoop.current().start()


def create_app():
    """Creates tornado application.

    Creates the routing in the application and returns the complete app.
    """
    # Define socket for both client and processor
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler)
    ]

    # Construct and serve the tornado application.
    return Application(handlers)


if __name__ == "__main__":
    main()
