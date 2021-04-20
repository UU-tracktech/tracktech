import ffmpeg
import pytest
import cv2
from processor.input.hls_capture import HlsCapture


class TestVideoForwarder:
    def setup_method(self):
        """Setup method that has url of the
        """
        self.hls_url = "http://localhost:80/testvid.m3u8"

    @pytest.fixture
    def hls_capture(self):
        return HlsCapture(self.hls_url)

    @pytest.mark.timeout(20)
    def test_hls_constructor(self, hls_capture):
        assert hls_capture.hls_url == self.hls_url
        assert hls_capture.thread.daemon

    @pytest.mark.timeout(20)
    def test_hls_opens(self, hls_capture):
        while not hls_capture.opened():
            continue

        hls_capture.close()

    @pytest.mark.timeout(20)
    def test_hls_opened_correctly(self, hls_capture):
        while not hls_capture.opened():
            continue

        assert hls_capture.cap_initialized
        assert hls_capture.cap

        hls_capture.close()

    @pytest.mark.timeout(20)
    def test_hls_closed_correctly(self, hls_capture):
        while not hls_capture.opened():
            continue

        hls_capture.close()

        assert not hls_capture.opened()

    @pytest.mark.timeout(20)
    def test_format_data(self):
        meta_data = ffmpeg.probe(self.hls_url)

        # Test format section
        assert meta_data.__contains__('format')
        format_data = meta_data['format']

        assert format_data.__contains__('start_time')
        assert format_data['filename'] == self.hls_url
        assert format_data['format_name'] == 'hls'

    @pytest.mark.timeout(20)
    def test_stream_data(self, hls_capture):
        meta_data = ffmpeg.probe(self.hls_url)
        streams_data = meta_data['streams']

        while not hls_capture.opened():
            continue

        meta_data_fps = int(streams_data[0]['avg_frame_rate'][:2])
        assert meta_data_fps == hls_capture.cap.get(cv2.CAP_PROP_FPS)
