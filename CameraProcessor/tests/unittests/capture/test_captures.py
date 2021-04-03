import pytest
import os
from src.input.icapture import ICapture
from src.input.image_capture import ImageCapture
from src.input.hls_capture import HlsCapture
from src.input.cam_capture import CamCapture


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
