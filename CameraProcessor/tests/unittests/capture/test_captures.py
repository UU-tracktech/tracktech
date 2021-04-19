import os
import pytest
from processor.input.icapture import ICapture
from processor.input.image_capture import ImageCapture
from processor.input.hls_capture import HlsCapture
from processor.input.cam_capture import CamCapture


class TestCaptures:

    @pytest.mark.timeout(10)
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        while not capture_implementation.opened():
            pass

    @pytest.mark.timeout(10)
    def test_next_frame(self, capture_implementation):
        """Asserts that you can get the next frame of the capture implementation

            Args:
                capture_implementation: see capture_implementation.

        """
        assert capture_implementation.get_next_frame()[0]

    @pytest.mark.timeout(10)
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        capture_implementation.close()
        while capture_implementation.opened():
            pass
