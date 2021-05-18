"""Unit test of the forwarder checks camera.py + json conversion

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from pytest import mark
from os import environ

from src.camera_handler import CameraHandler
from src.main import create_camera, create_stream_options, get_timeout_delay, get_remove_delay


class TestHandler(AsyncHTTPTestCase):

    def get_app(self):
        environ["CAMERA_URL"] = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
        environ["CAMERA_AUDIO"] = "true"

        environ["STREAM_LOW"] = 'true'

        return Application(
            [
                (r'/(.*)', CameraHandler, {'path': '/app/streams'})
            ],
            camera=create_camera(),
            stream_options=create_stream_options(),
            remove_delay=get_remove_delay(),
            timeout_delay=get_timeout_delay(),
        )

    def test_headers(self):
        """Tests hls stream header on certain properties
        """
        response = self.fetch('/')
        assert response.headers["Cache-control"] == "no-store"
        assert response.headers["Access-Control-Allow-Origin"] == "*"

    def test_valid_http_request(self):
        """Checks connection between forwarder and mock client with valid url
        """
        # Wait until main.py is up and running
        response = self.fetch('/stream.m3u8')

        # OK
        assert response.code == 200
