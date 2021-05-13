"""Tests stream_handler.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from tornado.testing import AsyncHTTPTestCase, AsyncTestCase
from processor.webhosting.stream_handler import StreamHandler
import tornado.testing
import tornado.web
import pytest


# This test uses coroutine style.
class MyTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
                    (r'/video_feed', StreamHandler)
                ])

    @pytest.mark.asyncio
    @tornado.testing.gen_test
    async def test_http_fetch(self):
        # ret = await self.http_client.fetch(r'/video_feed')
        client = self.http_client
        server = self.http_server
        self.fetch('video_feed')
        print()
        # response = yield client.fetch("http://www.tornadoweb.org")
        # Test contents of response
        # self.assertIn("FriendFeed", response.body)

    def test_homepage(self):
        # The following two lines are equivalent to
        #   response = self.fetch('/')
        # but are shown in full here to demonstrate explicit use
        # of self.stop and self.wait.
        self.http_client.fetch(self.get_url('/video_feed'), self.stop)
        response = self.wait(timeout=35)
        # test contents of response
        print()
#
# class TestHelloApp(AsyncHTTPTestCase):
#     def get_app(self):
#         return tornado.web.Application([
#             (r"/(.*\.html)?", HtmlPageHandler),
#         ])
#
#     def test_existing_html_file(self):
#         response = self.fetch('/')
#         self.assertEqual(response.code, 200)
#
#     def test_invalid_html_file(self):
#         response = self.fetch('/test.html')
#         assert str(response.body).__contains__('404')


# # This test uses coroutine style.
# class TestStreamHandler(AsyncHTTPTestCase):
#     def get_app(self):
#         return tornado.web.Application([
#             (r'/', StreamHandler)
#         ])
#
#     @pytest.mark.asyncio
#     @tornado.testing.gen_test
#     async def test_stream_fetch(self):
#         self.fetch('/')
#         # assert response.code == 200
#         # client = AsyncHTTPClient(self.io_loop)
#         # response = await client.fetch("/video_feed")
#         # Test contents of response
#         # self.assertIn("FriendFeed", response.body)
