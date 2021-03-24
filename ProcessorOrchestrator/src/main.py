import os
import ssl
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from client import ClientSocket
from processor import ProcessorSocket
from logger import LogHandler
define('port', default=8000, help='port to listen on')


def main():
    # Get ssl ready, if provided in the environment variables
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')
    use_tls = cert is not None and key is not None

    # Define socket for both client and processor
    handlers = [
        ('/client', ClientSocket),
        ('/processor', ProcessorSocket),
        ('/logs', LogHandler)
    ]

    # Construct and serve the tornado application.
    app = Application(handlers)

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


if __name__ == "__main__":
    main()
