"""Unit test of the forwarder checks camera.py and json conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from tornado.testing import AsyncHTTPSTestCase
from tornado import testing
import jwt

from tests.auth_setup import auth_setup


class AuthServerUnitTest(AsyncHTTPSTestCase):
    """Test the server when using auth."""

    def get_app(self):
        """Creates the application to test."""
        return auth_setup()

    def my_fetch(self, url, **kwargs):
        """Do a custom fetch, as the default one crashes.

        Args:
            url (str): extension url to fetch information from.
            **kwargs (Any): Other arguments given to the fetch command.
        """
        return self.http_client.fetch(self.get_url(url), raise_error=False, **kwargs)

    @testing.gen_test(timeout=10)
    def test_no_auth(self):
        """Check if a 403 is returned when no authentication is provided"""

        # Retrieve the stream file.
        response = yield self.my_fetch('/stream.m3u8')

        assert response.code == 403

    @testing.gen_test(timeout=10)
    def test_bad_auth(self):
        """Check if a 403 is returned when improper authentication is provided when required."""

        # Retrieve the stream file.
        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': 'Bearer RealFakeToken'}}
        )

        assert response.code == 403

    @testing.gen_test(timeout=10)
    def test_unimplemented_auth(self):
        """Check if a 403 is returned when improper authentication is provided when required."""

        # Retrieve the stream file.
        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': 'someprotocol RealFakeToken'}}
        )

        assert response.code == 403

    @testing.gen_test(timeout=10)
    def test_missing_auth(self):
        """Check if a 403 is returned when a single value is provided"""

        # Retrieve the stream file.
        response = yield self.my_fetch(
            '/stream.m3u8',
            **{'headers': {'Authorization': 'nospaceinhere'}}
        )

        assert response.code == 403

    @testing.gen_test(timeout=10)
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

        #alternatively, as query param
        response2 = yield self.my_fetch(f'/stream.m3u8?Bearer={token}')

        assert response2.code == 200

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
