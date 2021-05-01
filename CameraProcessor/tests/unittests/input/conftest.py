"""Fixtures and configurations available to other capture unit tests

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import pytest

from processor.input.hls_capture import HlsCapture
from processor.input.image_capture import ImageCapture
from processor.input.video_capture import VideoCapture
from tests.conftest import root_path


def __get_images_dir():
    """Get the path to the images directory.

    Returns: a string containing the file path to the image folder.

    """
    __images_dir = os.path.realpath(os.path.join(root_path, 'data/annotated/test/img1/'))
    return __images_dir


def __get_video():
    """Get the path to a video

    Returns: a string containing the file path to a video

    """
    __videos_dir = os.path.realpath(os.path.join(root_path, 'data/videos/test.mp4'))
    return __videos_dir


@pytest.fixture(params=[  # ImageCapture(__get_images_dir()),
                        VideoCapture(__get_video()),
                        HlsCapture()],
                ids=[  # "Image",
                     "video",
                     "HLS Stream"])
def capture_implementation(request):
    """ Defines capture_implementation as multiple implementations of iCapture,
    to be use in generic capture tests.

    Args:
        request: different implementations of capture.

    Returns: implementation of capture.

    """
    return request.param
