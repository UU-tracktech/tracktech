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


def create_camera():
    """
    Returns:
        A camera object containing the camera url and if it has any audio
    """
    return Camera(os.environ["CAMERA_URL"], os.environ["CAMERA_AUDIO"] == "true")


def create_stream_options():
    """

    Returns:
        StreamOptions: Load the stream options used for the conversion

    """
    return StreamOptions(
        os.environ.get("SEGMENT_SIZE") or "2",
        os.environ.get("SEGMENT_AMOUNT") or "5",
        os.environ.get("STREAM_ENCODING") or "libx264",
        os.environ.get("STREAM_LOW") == "true",
        os.environ.get("STREAM_MEDIUM") == "true",
        os.environ.get("STREAM_HIGH") == "true"
    )


def get_remove_delay():
    """
    Returns:
        float: How long the stream has no requests before stopping the conversion in seconds
    """
    return float(os.environ.get('REMOVE_DELAY') or '60.0')


def get_timeout_delay():
    """
    Returns:
        int: The maximum amount of seconds we will wait with removing stream files after stopping the conversion
    """
    return int(os.environ.get('TIMEOUT_DELAY') or '30')


def create_ssl_options():
    """
    Returns:
        ssl.SSLContext: an ssl_context to be used by the application
    """

    # Load environment variable path of certificate and its key
    cert = os.environ.get('SSL_CERT')
    key = os.environ.get('SSL_KEY')

    # If one if missing, return None and do not use ssl
    if cert is None or key is None:
        return None

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(cert, key)

    return ssl_ctx


def create_authenticator():
    """
    Returns:
        Auth: Auth object containing used to validate tokens
    """
    #
    public_key, audience, client_role =\
        os.environ.get('PUBLIC_KEY'), os.environ.get('AUDIENCE'), os.environ.get('CLIENT_ROLE')
    if public_key is None or audience is None or client_role is None:
        return None
    tornado.log.gen_log.info("using client token validation")
    return Auth(
        public_key_path=public_key,
        algorithms=['RS256'],
        audience=audience,
        role=client_role
    )


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

    # Create the web application with the camera handler and the public key
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ['STREAM_FOLDER']}),
        ],
        authenticator=create_authenticator(),
        camera=create_camera(),
        remove_delay=get_remove_delay(),
        timeout_delay=get_timeout_delay(),
        stream_options=create_stream_options()
    )

    # Load the ssl and port options
    ssl_options = create_ssl_options()
    port = 80 if ssl_options is None else 443
    ssl = 'without' if ssl_options is None else 'with'

    # Start the webserver
    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    http_server.listen(port)
    tornado.log.gen_log.info(f'listening on port {port}, {ssl} ssl')

    # Start the IO loop (used by tornado itself)
    tornado.ioloop.IOLoop.current().start()

