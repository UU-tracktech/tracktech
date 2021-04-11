import os

import pytest

from processor.input.cam_capture import CamCapture
from processor.input.hls_capture import HlsCapture
from processor.input.image_capture import ImageCapture


def __get_images_dir():
    """Get the path to the images directory.

    Returns: a string containing the file path to the image folder.

    """
    __root_dir = os.path.abspath(__file__ + '../../../../../')
    __folder_name = 'test'
    __images_dir = f'{__root_dir}/data/annotated/test/img1'
    return __images_dir


@pytest.fixture(params=[ImageCapture(__get_images_dir()), HlsCapture()], ids=["Image", "HLS Stream"])
def capture_implementation(request):
    """ Defines capture_implementation as multiple implementations of iCapture,
    to be use in generic capture tests.

    Args:
        request: different implementations of capture.

    Returns: implementation of capture.

    """
    return request.param
