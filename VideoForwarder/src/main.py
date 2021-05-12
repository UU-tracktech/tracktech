"""Starts the tornado webserver.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import sys
import os
import ssl
import tornado.httpserver
import tornado.web
import tornado.ioloop

from auth.auth import Auth
from src.logging_filter import LoggingFilter
from src.camera import Camera
from src.stream_options import StreamOptions
from src.camera_handler import CameraHandler

# pylint: disable=invalid-name
if __name__ == "__main__":
    # Setup for logging
    tornado.log.logging.basicConfig(
        filename='/app/src/main.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
        level=tornado.log.logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    tornado.log.gen_log.addHandler(tornado.log.logging.StreamHandler(sys.stdout))
    tornado.log.access_log.addHandler(tornado.log.logging.StreamHandler(sys.stdout))
    tornado.log.access_log.addFilter(LoggingFilter())

    tornado.log.gen_log.info('starting server')

    # Create the camera object from the environment variables
    camera = Camera(os.environ['CAMERA_URL'], os.environ['CAMERA_AUDIO'] == 'true')

    # How long the stream has no requests before stopping the conversion in seconds
    remove_delay = float(os.environ.get('REMOVE_DELAY') or '60.0')

    # The maximum amount of seconds we will wait with removing stream files after stopping the conversion
    timeout_delay = int(os.environ.get('TIMEOUT_DELAY') or '30')

    # Load the stream options used for the conversion
    stream_options = StreamOptions(
        os.environ.get('SEGMENT_SIZE') or '2',
        os.environ.get('SEGMENT_AMOUNT') or '5',
        os.environ.get('STREAM_ENCODING') or 'libx264',
        os.environ.get('STREAM_LOW') == 'true',
        os.environ.get('STREAM_MEDIUM') == 'true',
        os.environ.get('STREAM_HIGH') == 'true'
    )

    # Get the ssl certificate and key if supplied
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')

    # Get auth ready by reading the environment variables
    public_key, audience = os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE')
    authenticator = None
    if public_key is not None and audience is not None:
        client_role = os.environ.get('CLIENT_ROLE')
        if client_role is not None:
            tornado.log.gen_log.info("using client token validation")
            authenticator = Auth(
                public_key_path=public_key,
                algorithms=['RS256'],
                audience=audience,
                role=client_role
            )

    # Create the web application with the camera handler and the public key
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ],
        authenticator=authenticator,
        camera=camera,
        remove_delay=remove_delay,
        timeout_delay=timeout_delay,
        stream_options=stream_options
    )

    # If using tls, create a context and load the certificate and key in it
    if cert is not None and key is not None:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(cert, key)

        # Start the secure webserver on port 443
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(443)
        tornado.log.gen_log.info('listening on port 443 over https')

    # Else start the insecure webserver on port 80
    else:
        # Start the insecure webserver on port 80
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(80)
        tornado.log.gen_log.info('listening on port 80 over http')

    # Start the IO loop (used by tornado itself)
    tornado.ioloop.IOLoop.current().start()
