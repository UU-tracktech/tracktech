"""Tests html_page_handler.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from processor.webhosting.html_page_handler import HtmlPageHandler


class TestHtmlPageHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r"/(.*\.html)?", HtmlPageHandler),
        ])

    def test_existing_html_file(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_invalid_html_file(self):
        response = self.fetch('/test.html')
        self.assertIn("404", str(response.body))
