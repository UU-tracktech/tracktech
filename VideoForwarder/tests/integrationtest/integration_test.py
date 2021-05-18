"""Integration testing of forwarder with a dummy interface

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import pytest
from tornado.httpclient import HTTPClientError


# pylint: disable=attribute-defined-outside-init
class TestVideoForwarder:
    """Tests video forwarder http requests, headers and file behavior

    """
    def setup_method(self):
        """Setup method for testing

        """
        self.base_url = "http://video-forwarder:80/stream"
        # self.base_url = 'http://localhost:80/testvid'
        self.extension = ".m3u8"

        # Complete url of camera
        self.camera_url = self.base_url + self.extension
        self.stream_dir = "/streams"

    @pytest.mark.gen_test(timeout=15)
    @pytest.mark.asyncio
    async def test_invalid_http_request(self, http_client):
        """Checks connection between forwarder and mock client with invalid url

        Does not use pytest.raises since it cannot yield

        Args:
            http_client: Httpclient that connects

        """

        # Create connection with invalid url
        try:
            await http_client.fetch(f"{self.base_url}jibberish{self.extension}")
            assert False
        # Asserts exception is raised
        except HTTPClientError:
            assert True


    @pytest.mark.gen_test(timeout=15)
    @pytest.mark.asyncio
    async def test_generate_multiple_video_outputs(self, http_client):
        """Tests whether the stream generates several headers

        Args:
            http_client: Httpclient that connects

        """
        # Create a connection
        response_low_res = await http_client.fetch(f"{self.base_url}_V0{self.extension}")
        response_med_res = await http_client.fetch(f"{self.base_url}_V1{self.extension}")
        response_high_res = await http_client.fetch(f"{self.base_url}_V2{self.extension}")

        # Assert response is OK
        assert response_low_res.code == 200
        assert response_med_res.code == 200
        assert response_high_res.code == 200


if __name__ == '__main__':
    pytest.main(TestVideoForwarder)
