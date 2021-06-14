"""Unit test of the forwarder checks camera.py + json conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from os import environ
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado import testing
import jwt

from src.camera_handler import CameraHandler
from src.loading import create_camera,\
    create_stream_options,\
    create_authenticator,\
    get_wait_delay,\
    get_timeout_delay


class AuthServerUnitTest(AsyncHTTPTestCase):
    """Test the server when using auth."""

    def get_app(self):
        """Creates the application to test."""
        environ["CAMERA_URL"] = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
        environ["CAMERA_AUDIO"] = "true"

        environ["STREAM_LOW"] = 'true'
        environ["STREAM_HIGH"] = 'true'

        environ["PUBLIC_KEY"] = "/app/tests/files/public_key.pem"
        environ["AUDIENCE"] = "aud"
        environ["CLIENT_ROLE"] = "role"

        return Application(
            [
                (r'/(.*)', CameraHandler, {'path': '/app/streams3'})
            ],
            camera=create_camera(),
            stream_options=create_stream_options(),
            authenticator=create_authenticator(),
            remove_delay=1.0,
            timeout_delay=get_timeout_delay(),
            wait_delay=get_wait_delay()
        )

    def my_fetch(self, url, **kwargs):
        """Do a custom fetch, as the default one crashes.

        Args:
            url (str): extension url to fetch information from.
            **kwargs (Any): Other arguments given to the fetch command.
        """
        return self.http_client.fetch(self.get_url(url), raise_error=False, **kwargs)

    @testing.gen_test(timeout=10)
    def test_no_auth(self):
        """Check if a 200 is returned when no authentication is provided when it is not required."""

        # Retrieve the steam file.
        response = yield self.my_fetch('/stream.m3u8')

        assert response.code == 200

    @testing.gen_test(timeout=10)
    def test_bad_auth(self):
        """Check if a 403 is returned when improper authentication is provided when required."""

        # Retrieve the steam file.
        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': 'Bearer RealFakeToken'}}
        )

        assert response.code == 403

    @testing.gen_test(timeout=20)
    def test_auth(self):
        """Test if a 200 is returned with a completely valid token."""
        with open('/app/tests/files/private_key.pem', 'r') as file:
            key = file.read()

        token = jwt.encode(
            {
                'aud': [
                    'aud'
                ],
                'resource_access': {
                    'aud': {
                        'roles': [
                            'role'
                        ]
                    }
                }
            }, key, algorithm='RS256')

        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': f'Bearer {token}'}}
        )

        assert response.code == 200

    @testing.gen_test(timeout=10)
    def test_no_permission(self):
        """Test if a 401 is returned with a valid token but not the right role."""
        with open('/app/tests/files/private_key.pem', 'r') as file:
            key = file.read()

        token = jwt.encode(
            {
                'aud': [
                    'aud'
                ],
                'resource_access': {
                    'aud': {
                        'roles': [
                            'no role'
                        ]
                    }
                }
            }, key, algorithm='RS256')

        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': f'Bearer {token}'}}
        )

        assert response.code == 401
