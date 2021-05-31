"""Tests the captures.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.input.hls_capture import HlsCapture


# pylint: disable=attribute-defined-outside-init
class TestCaptures:
    """Tests the captures opening and closing.

    Attributes:
        capture (ICapture): Capture that gets tested
    """
    def setup_method(self):
        """Creates an empty capture."""
        self.capture = None

    def teardown_method(self):
        """Close down the capture."""
        if self.capture is not None:
            self.capture.close()

    @pytest.mark.timeout(60)
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation (ICapture): Uninitialized capture.
        """
        self.capture = capture_implementation()

        while not self.capture.opened():
            pass

    @pytest.mark.timeout(60)
    def test_next_frame(self, capture_implementation):
        """Asserts that you can get the next frame of the capture implementation.

        Args:
            capture_implementation (ICapture): Uninitialized capture.
        """
        self.capture = capture_implementation()

        while not self.capture.get_next_frame()[0]:
            pass

    @pytest.mark.timeout(60)
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation (ICapture): Uninitialized capture.
        """
        self.capture = capture_implementation()

        while not self.capture.opened():
            pass

        # Close the capture.
        self.capture.close()
        while self.capture.opened():
            pass

        # Cannot get a next frame after closing.
        assert not self.capture.get_next_frame()[0]

    @pytest.mark.timeout(60)
    def test_invalid_url(self):
        """Checks the behavior when the HlsCapture does not get a valid url."""
        # Invalid hls stream url throws exception.
        with pytest.raises(TimeoutError):
            self.capture = HlsCapture('http://181.83.10.9:8001/mjpg/video.mjpg', 2)
