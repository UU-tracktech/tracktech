"""Starts the tornado webserver.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import sys
import os
import tornado.httpserver
import tornado.web
import tornado.ioloop

from src.loading import create_authenticator, create_camera, create_stream_options, create_ssl_options,\
    get_remove_delay, get_timeout_delay, get_wait_delay
from src.logging_filter import LoggingFilter
from src.camera_handler import CameraHandler

# pylint: disable=invalid-name
if __name__ == "__main__":
    # Setup for logging.
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

    # Create the web application with the camera handler and the public key.
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ.get('STREAM_FOLDER') or 'app/streams'}),
        ],
        authenticator=create_authenticator(),
        camera=create_camera(),
        remove_delay=get_remove_delay(),
        timeout_delay=get_timeout_delay(),
        wait_delay=get_wait_delay(),
        stream_options=create_stream_options()
    )

    # Load the ssl and port options.
    ssl_options = create_ssl_options()
    port = 80 if ssl_options is None else 443
    ssl = 'without' if ssl_options is None else 'with'

    # Start the webserver.
    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    http_server.listen(port)
    tornado.log.gen_log.info(f'listening on port {port}, {ssl} ssl')

    # Start the IO loop (used by tornado itself).
    tornado.ioloop.IOLoop.current().start()
