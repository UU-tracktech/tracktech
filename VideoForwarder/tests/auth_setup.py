"""Unit test helper function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from os import environ
from tornado.web import Application

from src.camera_handler import CameraHandler
from src.loading import create_camera, \
    create_stream_options, \
    create_authenticator, \
    get_wait_delay, \
    get_timeout_delay


def auth_setup():
    """Gets the ffmpeg conversion command for the camera stream that can be started later on.

    Returns:
        Application: The application that can be used for authenticated server tests.
    """
    environ["CAMERA_URL"] = "rtmp://localhost:1931/stream"
    environ["CAMERA_AUDIO"] = "false"

    environ["STREAM_LOW"] = 'true'
    environ["STREAM_HIGH"] = 'true'

    environ["PUBLIC_KEY"] = "/app/tests/files/public_key.pem"
    environ["AUDIENCE"] = "aud"
    environ["CLIENT_ROLE"] = "role"

    return Application(
        [
            (r'/(.*)', CameraHandler, {'path': '/app/streams1'})
        ],
        camera=create_camera(),
        stream_options=create_stream_options(),
        authenticator=create_authenticator(),
        remove_delay=1.0,
        timeout_delay=get_timeout_delay(),
        wait_delay=get_wait_delay()
    )
