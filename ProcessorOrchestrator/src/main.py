"""Entry point of the application

This file sets up the tornado application.
"""
import os
import ssl

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from auth.auth import Auth
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

    # Get auth ready by reading the environment variables 
    public_key, audience, role = os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE'), os.environ.get('ROLE')
    auth = None
    if public_key is not None and audience is not None and role is not None:
        print("using token validation")
        auth = Auth(public_key_path=public_key, algorithms=['RS256'], audience=audience, role=role)

    app = create_app(auth)

    if use_tls:
        # Create a ssl context
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Create a http server, with optional ssl.
        http_server = HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        print('listening over https')

    else:
        # Create a http server, with optional ssl.
        http_server = HTTPServer(app)
        http_server.listen(80)
        print('listening over http')

    IOLoop.current().start()


def create_app(auth):
    """Creates tornado application.

    Creates the routing in the application and returns the complete app.

    Args:
        auth:  A auth object containing identity provider information
    """
    # Define socket for both client and processor
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler)
    ]
    
    # Construct and serve the tornado application.
    return Application(handlers, auth=auth)


if __name__ == "__main__":
    main()
