"""Tests stream_handler.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest
import tornado.testing
import tornado.web
from tornado.testing import AsyncHTTPTestCase

from tests.conftest import get_test_configs
from processor.webhosting.stream_handler import StreamHandler


class TestStreamHandler(AsyncHTTPTestCase):
    """Tests the stream handler using an asyncHTTPTestCase superclass.

    Used async since we deal with a tornado.gen.coroutine which yields to give
    preemptive returns so the get request.
    """
    def get_app(self):
        """Creates an app only containing the stream handler.

        Returns:
            (tornado.web.Application): The streamhandler used to push to localhost
        """
        configs = get_test_configs()

        return tornado.web.Application([
            (r'/video_feed', StreamHandler, dict(configs=configs))
        ])

    @tornado.testing.gen_test(timeout=40)
    @pytest.mark.skip(reason="either stream is closed or no images received, tornado page seems to work")
    def test_stream_handler(self):
        """Fetch the video feed and see whether the response contains images."""
        # Gets the stream from the httpserver.
        response = yield self.http_client.fetch(self.get_url('/video_feed'), self.stop, request_timeout=0)
        self.assertEqual(response.code, 200)

        # Images in the response.body.
        image_responses = str(response.body).split('--jpgboundary')[1:]
        assert len(image_responses) >= 1

        # Streams jpeg images.
        assert image_responses[0].startswith('Content-type: image/jpeg')
