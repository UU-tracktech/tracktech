import pytest
import os
from src.input.image_capture import ImageCapture
from src.input.hls_capture import HlsCapture
from src.input.cam_capture import CamCapture

root_dir = os.path.abspath(__file__ + '../../../../../')
folder_name = 'test'
images_dir = f'{root_dir}\\data\\annotated\\{folder_name}\\img1'


class TestCaptures:
    @pytest.fixture(params=[ImageCapture(images_dir), HlsCapture(), CamCapture()])
    def capture_implementation(self, request):
        """ Defines capture_implementation as multiple implementations of iCapture, to be use in generic capture tests.

        Args:
            request: different implementations of capture.

        Returns: implementation of capture.

        """
        return request.param

    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        assert capture_implementation.opened()

    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        capture_implementation.close()
        assert not capture_implementation.opened()
