"""Integration testing of forwarder with a dummy interface

"""

import time
import os
import pytest
import tornado.web
from tornado.simple_httpclient import HTTPStreamClosedError


class MainHandler(tornado.web.RequestHandler):
    """Tornado web application

    """
    def get(self):
        """Empty get

        """
        self.write("")


application = tornado.web.Application([
    (r"/", MainHandler),
])


@pytest.fixture
def app():
    """Creates application

    Return:
         application: tornado application
    """
    return application


# pylint: disable=attribute-defined-outside-init
class TestVideoForwarder:
    """Tests video forwarder http requests, headers and file behavior

    """
    def setup_method(self):
        """Setup method for testing

        """
        self.port = 80
        self.camera = 'testvid'
        self.base_url = 'http://localhost'
        self.extension = 'm3u8'
        self.camera_url = f'{self.base_url}:{self.port}/{self.camera}.{self.extension}'

        self.stream_dir = '/streams'
        self.camera_versions = ['_V0', '_V1', '_V2']

    @pytest.mark.gen_test(timeout=15)
    def test_valid_http_request(self, http_client):
        """Checks connection between forwarder and mock client with valid url

        Args:
            http_client: Httpclient that connects

        """
        response = yield http_client.fetch(self.camera_url)

        # OK
        assert response.code == 200

    @pytest.mark.gen_test(timeout=15)
    def test_invalid_http_request(self, http_client):
        """Checks connection between forwarder and mock client with invalid url

        Does not use pytest.raises since it cannot yield

        Args:
            http_client: Httpclient that connects

        """

        # Create connection with invalid url
        try:
            yield http_client.fetch(self.camera_url)
            assert False
        # Asserts exception is raised
        except HTTPStreamClosedError:
            assert True

    @pytest.mark.gen_test(timeout=15)
    def test_headers(self, http_client):
        """Tests hls stream header on certain properties

        Args:
            http_client: Httpclient that connects

        """
        response = yield http_client.fetch(self.camera_url)
        assert response.headers['Cache-control'] == 'no-store'
        assert response.headers['Access-Control-Allow-Origin'] == '*'

    @pytest.mark.gen_test(timeout=15)
    def test_generate_multiple_video_outputs(self, http_client):
        """Tests whether the stream generates several headers

        Args:
            http_client: Httpclient that connects

        """
        # Create camera with versions
        camera = self.camera
        versions = self.camera_versions
        camera_versions = [camera + version for version in versions]
        version_counter = 0

        # Create a connection
        yield http_client.fetch(self.camera_url)

        # Foreach camera version
        for camera_version in camera_versions:
            # List all files inside directory that start with current version
            for file in os.listdir(self.stream_dir):
                if file.startswith(camera_version):
                    version_counter += 1
                    break

        # Asserts number of versions is correct
        assert version_counter == len(versions)

    @pytest.mark.gen_test(timeout=15)
    def test_delete_files(self, http_client):
        """Tests whether files are properly deleted after 61 seconds

        Args:
            http_client: Httpclient that connects

        """
        # Create camera
        camera = self.camera

        # Create connection
        yield http_client.fetch(self.camera_url)

        # After 60 seconds files are deleted on server
        time.sleep(61)

        # Checks whether files are actually deleted
        for file in os.listdir(self.stream_dir):
            if file.startswith(camera):
                assert False


if __name__ == '__main__':
    pytest.main(TestVideoForwarder)
