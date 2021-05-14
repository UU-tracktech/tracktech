"""Tests stream_handler.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import tornado.testing
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from processor.webhosting.stream_handler import StreamHandler


# This test uses coroutine style.
class TestStreamHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r'/video_feed', StreamHandler)
        ])

    @tornado.testing.gen_test(timeout=20)
    def test_stream_handler(self):
        # Gets the stream from the httpserver
        response = yield self.http_client.fetch(self.get_url('/video_feed'), self.stop)
        self.assertEqual(response.code, 200)

        # Images in the response.body
        image_responses = str(response.body).split('--jpgboundary')[1:]
        assert len(image_responses) >= 1

        # Streams jpeg images
        assert image_responses[0].startswith('Content-type: image/jpeg')
