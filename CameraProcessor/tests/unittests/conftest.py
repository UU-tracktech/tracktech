"""Fixtures and configurations available to all unittests.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
import numpy as np
import cv2

from tests.conftest import root_path


@pytest.fixture
def img():
    """Fixture for a blank image.

    Returns:
        np.ndarray: a numpy array representing an image, in this case a blank one.
    """
    image_size = 200
    # Create an empty white image.
    image = np.zeros((image_size, image_size, 3), np.uint8)
    image.fill(255)
    return image


@pytest.fixture
def small_frame():
    """Fixture for a small frame loaded with opencv.

    Returns:
        np.ndarray: Opencv frame from test data.
    """
    __image_name = f'{root_path}/data/tests/unittests/small_image.jpg'
    return cv2.imread(__image_name)


@pytest.fixture
def large_frame():
    """Fixture that gets a big frame loaded with opencv.

    Returns:
        np.ndarray: Opencv frame from test data.
    """
    __image_name = f'{root_path}/data/tests/unittests/big_image.jpg'
    return cv2.imread(__image_name)
