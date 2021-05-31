"""Tests html_page_handler.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from processor.webhosting.html_page_handler import HtmlPageHandler

from tests.conftest import get_test_configs


class TestHtmlPageHandler(AsyncHTTPTestCase):
    """Test the html page handler whether the pages gets retrieved correctly."""
    def get_app(self):
        """Creates the tornado the app.

        Returns:
            (tornado.web.Application): Html page handler that gets started by the AsyncHTTPTestCase.
        """
        configs = get_test_configs()

        return tornado.web.Application([
            # HTML file regex pattern.
            (r"/(.*\.html)?", HtmlPageHandler, dict(configs=configs)),
        ])

    def test_default_html_file(self):
        """Test rendering of an existing html file."""
        # Fetches index.html, which is the default.
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_existing_html_file(self):
        """Test rendering of an existing html file."""
        # Fetches index.html.
        response = self.fetch('/index.html')
        self.assertEqual(response.code, 200)

    def test_invalid_html_file(self):
        """Tests whether an invalid file gives back the error template."""
        response = self.fetch('/test.html')
        # Error page gets rendered.
        self.assertEqual(response.code, 200)
        self.assertIn("404", str(response.body))
