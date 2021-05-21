"""Fixtures and configurations available to utils tests

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest
import numpy as np
import cv2

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.utils.draw import draw_tracking_boxes, draw_detection_boxes

from tests.conftest import root_path

X0, X1 = 60, 120
Y0, Y1 = 120, 180
IMG_SIZE = 200


@pytest.fixture
def img():
    """Fixture for a blank image

    Returns:
        np.ndarray: a numpy array representing an image, in this case a blank one

    """
    # Create an empty white image
    image = np.zeros((IMG_SIZE, IMG_SIZE, 3), np.uint8)
    image.fill(255)
    return image


@pytest.fixture
def small_frame():
    """Fixture for a small frame loaded with opencv

    Returns (frame):
        Opencv frame from test data
    """
    __image_name = f'{root_path}/data/tests/unittests/small_image.jpg'
    return cv2.imread(__image_name)


@pytest.fixture
def large_frame():
    """Fixture that gets a big frame loaded with opencv

    Returns (frame):
        Opencv frame from test data
    """
    __image_name = f'{root_path}/data/tests/unittests/big_image.jpg'
    return cv2.imread(__image_name)


@pytest.fixture
def bbox():
    """Fixture for a bounding box

    Returns:
          BoundingBox: A boundingbox for use in testing
    """
    # Create a dummy bounding box
    return BoundingBox(1, Rectangle(round(float(X0 / IMG_SIZE), 1),
                                    round(float(Y0 / IMG_SIZE), 1),
                                    round(float(X1 / IMG_SIZE), 1),
                                    round(float(Y1 / IMG_SIZE), 1)),
                       "Bob", 0.50)


@pytest.fixture(params=[
    {"func": draw_detection_boxes,
     "text": f'Bob {round(float(0.50), 2)}',
     "seed": "Bob"
     },
    {"func": draw_tracking_boxes,
     "text": "1",
     "seed": 1
     }],
    ids=["Detection", "Tracking"])
def func_text_seed(request):
    """Fixture for the function, text, and seed

    """
    return request.param
