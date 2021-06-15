"""Unit test of the forwarder checks camera.py and json conversion.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from tornado.testing import AsyncHTTPTestCase
from tornado import testing

from tests.auth_setup import auth_setup


class AuthHttpServerUnitTest(AsyncHTTPTestCase):
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
        """Check if a 200 is returned when no authentication is provided and not needed (for local only)."""

        # Retrieve the stream file.
        response = yield self.my_fetch('/stream.m3u8')

        assert response.code == 200
