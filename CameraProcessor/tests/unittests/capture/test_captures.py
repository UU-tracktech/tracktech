import os
import pytest
from processor.input.icapture import ICapture
from processor.input.image_capture import ImageCapture
from processor.input.hls_capture import HlsCapture
from processor.input.cam_capture import CamCapture


class TestCaptures:

    @pytest.mark.skip(reason="Skipping for CI/CD Test")
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        assert capture_implementation.opened()

    @pytest.mark.skip
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        capture_implementation.close()
        assert not capture_implementation.opened()
