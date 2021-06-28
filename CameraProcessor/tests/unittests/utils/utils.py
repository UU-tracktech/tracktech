"""Util methods that are available to other unit tests as well.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import cv2
from tests.conftest import root_path


def is_same_frame_image(original, second):
    """Checks if two frames images are the same.

    Args:
        original (Frame): The original frame.
        second (Frame): Frame to compare the original frame to.

    Returns:
        bool: Whether two frames are the same.
    """
    # Calculate difference.
    difference = cv2.subtract(original, second)
    blue, green, red = cv2.split(difference)

    # Return true if it is the same image.
    return cv2.countNonZero(blue) == 0 and cv2.countNonZero(green) == 0 and cv2.countNonZero(red) == 0


def get_sample_frame():
    """So the test has access to an example frame in the detection object.

    Returns:
        numpy.ndarray: opencv frame from test data.
    """
    __images_name = f'{root_path}/data/tests/unittests/images/000001.jpg'
    return cv2.imread(__images_name)
