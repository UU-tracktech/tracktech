"""Fixtures and configurations available to other capture unit tests

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest

from processor.utils.config_parser import ConfigParser
from processor.input.hls_capture import HlsCapture
from processor.input.video_capture import VideoCapture
from processor.input.image_capture import ImageCapture


def __get_images_dir():
    """Get the path to the images directory.

    Returns: a string containing the file path to the image folder.

    """
    config_parser = ConfigParser('configs.ini')
    return config_parser.configs['Accuracy']['source_path']


def __get_video_path():
    """Get the path to a video

    Returns: a string containing the file path to a video

    """
    config_parser = ConfigParser('configs.ini')
    print(f"video path: {config_parser.configs['Yolov5']['test_path']}")

    return config_parser.configs['Yolov5']['test_path']


@pytest.fixture(scope="class",
                params=[lambda: ImageCapture(__get_images_dir()),
                        lambda: VideoCapture(__get_video_path()),
                        lambda: HlsCapture()
                        ],
                ids=["Image",
                     "video",
                     "HLS Stream"
                     ])
def capture_implementation(request):
    """ Defines capture_implementation as multiple implementations of iCapture,
    to be use in generic capture tests.

    Args:
        request: different implementations of capture.

    Returns: implementation of capture.

    """
    return request.param
