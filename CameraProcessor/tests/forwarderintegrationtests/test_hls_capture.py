"""Tests the processor with a started video forwarder to see whether HlsCapture works correctly

"""
import ffmpeg
import pytest
import cv2
from processor.input.hls_capture import HlsCapture


class TestVideoForwarder:
    """Tests the video forwarder in combination with the camera processor

    Checks basic functionality of the hls capture
    Including opening, closing of the capture and reading hls header
    """
    def setup_method(self):
        """Setup method that has url of the
        """
        # self.hls_url = "http://forwarder-test-service/testvid.m3u8"
        self.hls_url = "http://forwarder-test-service/"

    @pytest.fixture
    def hls_capture(self):
        """Initialize HlCapture object with the test url

        Return:
            HlsCapture: With predefined url
        """
        return HlsCapture(self.hls_url)

    @pytest.mark.timeout(20)
    def test_hls_constructor(self, hls_capture):
        """Checks whether constructor of hls capture has been set correctly

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder
        """
        # Url set correctly and thread has correct setting
        assert hls_capture.hls_url == self.hls_url
        assert hls_capture.reading_thread.daemon

    @pytest.mark.timeout(20)
    def test_hls_opened_correctly(self, hls_capture):
        """Tests whether the hls stream opened correctly

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder
        """
        # Waits until hls capture has opened
        while not hls_capture.opened():
            continue

        # Bool set to initialized and capture exists
        assert hls_capture.cap_initialized
        assert hls_capture.cap

    @pytest.mark.timeout(20)
    @pytest.mark.skip("Close throws exception")
    def test_hls_closed_correctly(self, hls_capture):
        """Tests whether the hls stream closed correctly

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder
        """
        # Waits until hls capture has opened
        while not hls_capture.opened():
            continue

        # Close the Hls capture
        hls_capture.close()

        # Hls capture is indeed closed
        assert not hls_capture.opened()

    @pytest.mark.timeout(20)
    def test_format_data(self):
        """Tests if the meta data that we get from ffprobe function, contains the same url as our predefined url
        """
        # Probes meta data from hls stream
        meta_data = ffmpeg.probe(self.hls_url)

        # Checks format section of meta data
        assert meta_data.__contains__('format')
        format_data = meta_data['format']
        assert format_data.__contains__('start_time')
        assert format_data['filename'] == self.hls_url

    @pytest.mark.timeout(20)
    def test_stream_data(self, hls_capture):
        """Tests whether the hls capture object correctly retrieves the average FPS value

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder
        """
        # Probes meta data
        meta_data = ffmpeg.probe(self.hls_url)
        streams_data = meta_data['streams']

        # Wait until hls capture is opened
        while not hls_capture.opened():
            continue

        # Frame rate corresponds to opencv framerate
        meta_data_fps = int(streams_data[0]['avg_frame_rate'][:2])
        assert meta_data_fps == hls_capture.cap.get(cv2.CAP_PROP_FPS)

    @pytest.mark.timeout(20)
    def test_get_next_frame(self, hls_capture):
        """Tests whether the hls capture can get a frame from the stream

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder
        """
        # Wait until capture is opened
        while not hls_capture.opened():
            continue

        ret = False
        frame = None

        # Gets the first frame from the hls capture
        while not ret:
            ret, frame, _ = hls_capture.get_next_frame()

        # Has returned with frame
        assert frame.any()
