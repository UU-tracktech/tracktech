"""Starts the tornado webserver.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import sys
import os
from logging import info
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

    tornado.log.access_log.addHandler(tornado.log.logging.StreamHandler(sys.stdout))
    tornado.log.access_log.addFilter(LoggingFilter())

    info('starting server')

    # Create the web application with the camera handler and the public key.
    app = tornado.web.Application(
        [
            (r'/(.*)', CameraHandler, {'path': os.environ.get('STREAM_FOLDER') or '/app/streams'}),
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
    if ssl_options is not None:
        https_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
        https_server.listen(443)
        info('listening over https')

    # Start the webserver.
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(80)
    info('listening over http')

    # Start the IO loop (used by tornado itself).
    tornado.ioloop.IOLoop.current().start()
