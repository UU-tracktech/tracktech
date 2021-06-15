"""Unit test of the forwarder checks camera.py and json conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from os import environ
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado import testing

from src.camera_handler import CameraHandler
from src.main import create_camera, create_stream_options


class SlowServerUnitTest(AsyncHTTPTestCase):
    """Test the server when unable to connect to the stream quickly enough."""

    def get_app(self):
        """Creates the application to test."""
        environ["CAMERA_URL"] = "rtmp://localhost/stream3"
        environ["CAMERA_AUDIO"] = "false"

        environ["STREAM_LOW"] = 'false'
        environ["STREAM_MEDIUM"] = 'false'

        return Application(
            [
                (r'/(.*)', CameraHandler, {'path': '/app/streams2'})
            ],
            camera=create_camera(),
            stream_options=create_stream_options(),
            remove_delay=1.0,
            timeout_delay=1,
            wait_delay=0
        )

    def my_fetch(self, url):
        """Do a custom fetch, as the default one crashes.

        Args:
            url (str): Url to connect to.
        """
        return self.http_client.fetch(self.get_url(url), raise_error=False)

    @testing.gen_test(timeout=20)
    def test_timeout(self):
        """Check not found is returned when the stream cannot be started within the timeout."""

        # Retrieve the steam file.
        response = yield self.my_fetch('/stream.m3u8')

        # Check if the response is Not Found.
        assert response.code == 404
