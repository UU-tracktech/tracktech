import pytest
import tornado.web
import time
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")

application = tornado.web.Application([
    (r"/", MainHandler),
])

@pytest.fixture
def app():
    return application

class TestVideoForwarder():
    def setup_method(self):
        self.port = 80
        self.camera = 'testvid'
        self.baseURL = 'http://localhost'
        self.extension = 'm3u8'
        self.camera_url = f'{self.baseURL}:{self.port}/{self.camera}.{self.extension}'

        self.stream_dir = '/streams'
        self.camera_versions = ['_V0', '_V1', '_V2']

    @pytest.mark.gen_test(timeout=15)
    def test_valid_http_request(self, http_client):
        response = yield http_client.fetch(self.camera_url)
        assert response.code == 200

    @pytest.mark.gen_test(timeout=15)
    def test_invalid_http_request(self, http_client):
        try:
            yield http_client.fetch(self.camera_url)
            assert False
        except Exception as e:
            assert True

    @pytest.mark.gen_test(timeout=15)
    def test_cache_control_header(self, http_client):
        response = yield http_client.fetch(self.camera_url)
        assert response.headers['Cache-control'] == 'no-store'

    @pytest.mark.gen_test(timeout=15)
    def test_access_control_allow_origin(self, http_client):
        response = yield http_client.fetch(self.camera_url)
        assert response.headers['Access-Control-Allow-Origin'] == '*'


    @pytest.mark.gen_test(timeout=15)
    def test_generate_multiple_video_outputs(self, http_client):
        camera = self.camera
        versions = self.camera_versions
        camera_versions = [camera + version for version in versions]
        version_counter = 0
        yield http_client.fetch(self.camera_url)
        for camera_version in camera_versions:
            for file in os.listdir(self.stream_dir):
                if file.startswith(camera_version):
                    version_counter += 1
                    break
        assert version_counter == len(versions)

    # @pytest.mark.gen_test(timeout=15)
    # def test_delete_files(self, http_client):
    #     camera = self.camera
    #     yield http_client.fetch(self.camera_url)
    #     time.sleep(61)
    #     for file in os.listdir(self.stream_dir):
    #         if file.startswith(camera):
    #             assert False
if __name__ == '__main__':
    pytest.main(TestVideoForwarder)













