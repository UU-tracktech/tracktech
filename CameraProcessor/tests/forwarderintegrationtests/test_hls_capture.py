"""Tests the processor with a started video forwarder to see whether HlsCapture works correctly.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import ffmpeg
import pytest

from processor.input.hls_capture import HlsCapture


# pylint: disable=attribute-defined-outside-init
class TestHlsCapture:
    """Tests the video forwarder in combination with the camera processor.

    Checks basic functionality of the hls capture
    Including opening, closing of the capture and reading hls header.

    Attributes:
        hls_url (str): Url of the video forwarder HLS stream.
    """
    def setup_method(self):
        """Setup method that has url of the video forwarder."""
        self.hls_url = "http://forwarder-test-service:80/stream.m3u8"

    @pytest.fixture
    def hls_capture(self):
        """Initialize HlsCapture object with the test url.

        Returns:
            HlsCapture: With predefined url of the video forwarder
        """
        return HlsCapture(self.hls_url)

    @pytest.mark.timeout(60)
    def test_hls_opened_correctly(self, hls_capture):
        """Tests whether the hls stream opened correctly.

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder.
        """
        # Waits until hls capture has opened.
        while not hls_capture.opened():
            continue

        # Close the Hls capture.
        hls_capture.close()

    @pytest.mark.timeout(60)
    def test_hls_closed_correctly(self, hls_capture):
        """Tests whether the hls stream closed correctly.

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder.
        """
        # Waits until hls capture has opened.
        while not hls_capture.opened():
            continue

        # Close the Hls capture.
        hls_capture.close()

        # Hls capture is indeed closed.
        assert not hls_capture.opened()

    @pytest.mark.timeout(60)
    def test_format_data(self):
        """Tests if the metadata that we get from ffprobe function, contains the same url as our predefined URL."""
        # Probes meta data from hls stream.
        meta_data = ffmpeg.probe(self.hls_url)

        # Checks format section of meta data.
        assert meta_data.__contains__('format')
        format_data = meta_data['format']
        assert format_data.__contains__('start_time')
        assert format_data['filename'] == self.hls_url

    @pytest.mark.timeout(60)
    def test_stream_data(self, hls_capture):
        """Tests whether the hls capture object correctly retrieves the average FPS value.

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder.
        """
        # Probes meta data.
        meta_data = ffmpeg.probe(self.hls_url)
        streams_data = meta_data['streams']

        # Wait until hls capture is opened.
        while not hls_capture.opened():
            continue

        # Frame rate corresponds to opencv framerate.
        meta_data_fps = int(streams_data[0]['avg_frame_rate'][:2])
        assert meta_data_fps == hls_capture.fps

        # Close the Hls capture.
        hls_capture.close()

    @pytest.mark.timeout(60)
    def test_get_next_frame(self, hls_capture):
        """Tests whether the hls capture can get a frame from the stream.

        Args:
            hls_capture (HlsCapture): Initialized hls capture with predefined link to forwarder.
        """
        # Wait until capture is opened.
        while not hls_capture.opened():
            continue

        ret = False
        frame_obj = None

        # Gets the first frame from the hls capture.
        while not ret:
            ret, frame_obj = hls_capture.get_next_frame()

        # Has returned with frame.
        assert frame_obj is not None

        # Close the Hls capture.
        hls_capture.close()
