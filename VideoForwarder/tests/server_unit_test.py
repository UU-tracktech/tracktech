"""Unit test of the forwarder checks camera.py and json conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from time import sleep
from os import environ
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado import testing

from src.camera_handler import CameraHandler
from src.main import create_camera, create_stream_options, get_wait_delay, get_timeout_delay


class ServerUnitTest(AsyncHTTPTestCase):
    """Test the server without authentication."""

    def get_app(self):
        """Creates the application to test."""
        environ['CAMERA_URL'] = 'rtmp://localhost:1932/stream'
        environ['CAMERA_AUDIO'] = 'false'

        environ['STREAM_LOW'] = 'true'
        environ['STREAM_MEDIUM'] = 'true'
        environ['STREAM_HIGH'] = 'false'

        return Application(
            [
                (r'/(.*)', CameraHandler, {'path': '/app/streams2'})
            ],
            camera=create_camera(),
            stream_options=create_stream_options(),
            remove_delay=10.0,
            timeout_delay=get_timeout_delay(),
            wait_delay=get_wait_delay()
        )

    def my_fetch(self, url):
        """Do a custom fetch, as the default one crashes.

        Args:
            url (str): Extension to connect to.
        """
        return self.http_client.fetch(self.get_url(url), raise_error=False)

    @testing.gen_test(timeout=10)
    def test_headers(self):
        """Tests hls stream header on certain properties."""

        response = yield self.my_fetch('/')
        assert response.headers['Cache-control'] == 'no-store'
        assert response.headers['Access-Control-Allow-Origin'] == '*'

    @testing.gen_test(timeout=10)
    def test_valid_http_request(self):
        """Check if a stream can be requested."""

        # Retrieve the steam file.
        response = yield self.my_fetch('/stream.m3u8')

        # Check if the response is okay.
        assert response.code == 200

    @testing.gen_test(timeout=10)
    def test_stop_callback(self):
        """Check if the cancel callback gets stopped."""

        # Retrieve the steam file.
        response1 = yield self.my_fetch('/stream.m3u8')
        sleep(5)
        response2 = yield self.my_fetch('/stream.m3u8')

        # Check if the response is okay.
        assert response1.code == 200
        assert response2.code == 200

    @testing.gen_test(timeout=10)
    def test_invalid_http_request(self):
        """Checks connection between forwarder and mock client with invalid URL.

        Does not use pytest.raises since it cannot yield.
        """

        # Create connection with invalid url.
        response = yield self.my_fetch('/realfakestream.ts')

        # Check if the request fails.
        assert response.code == 404

    @testing.gen_test(timeout=10)
    def test_generate_multiple_video_outputs(self):
        """Tests whether the stream generates several headers."""
        # Create a connection.
        response_low_res = yield self.my_fetch('/stream_V0.m3u8')
        response_med_res = yield self.my_fetch('/stream_V1.m3u8')
        response_high_res = yield self.my_fetch('/stream_V2.m3u8')

        # Assert response is OK.
        assert response_low_res.code == 200
        assert response_med_res.code == 200

        # Assert the response is Not Found.
        assert response_high_res.code == 404

    @testing.gen_test(timeout=10)
    def test_options(self):
        """Tests whether 204 is returned when using options instead of get (for preflight checks)."""
        # Create a connection.
        response = yield self.http_client.fetch(self.get_url('/stream.m3u8'), method='OPTIONS', raise_error=False)

        # Assert the response is empty.
        assert response.code == 204
