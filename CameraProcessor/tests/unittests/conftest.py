"""Fixtures and configurations available to all unittests.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
import numpy as np
import cv2

from tests.conftest import root_path
from processor.data_object.rectangle import Rectangle
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes


@pytest.fixture
def bbox():
    """Fixture for an example bounding box.

    Returns:
        BoundingBox: A BoundingBox for use in testing.
    """
    img_size = 200
    x0, x1 = 60, 120
    y0, y1 = 120, 180
    # Create a dummy bounding box.
    return BoundingBox(1, Rectangle(round(float(x0 / img_size), 1),
                                    round(float(y0 / img_size), 1),
                                    round(float(x1 / img_size), 1),
                                    round(float(y1 / img_size), 1)),
                       "Bob", 0.50)


@pytest.fixture
def bboxes():
    """Fixture for an example BoundingBoxes object.

    Returns:
        (BoundingBoxes): BoundingBoxes object.
    """
    box1 = BoundingBox(1, Rectangle(0, 0.5, 0.75, 1), "person", 0.5, object_id=5)
    box2 = BoundingBox(4, Rectangle(0.1, 0.25, 0.5, 0.9), "car", 0.75, object_id=15)
    box3 = BoundingBox(2, Rectangle(0.2, 0.3, 0.6, 0.8), "person", 0.8, object_id=10)
    return BoundingBoxes([box1, box2, box3], '12')

@pytest.fixture
def bounding_boxes_object_dict():
    """Fixture for an example BoundingBoxes list.

    Returns:
        ([BoundingBoxes]): list of BoundingBoxes objects.
    """
    box1 = BoundingBox(6, Rectangle(0, 0.6, 0.45, 1), "person", 0.5, object_id=6)
    box2 = BoundingBox(78, Rectangle(0.1, 0.23, 0.5, 0.4), "car", 0.75, object_id=18)
    box3 = BoundingBox(678, Rectangle(0.2, 0.6, 0.7, 0.8), "person", 0.8, object_id=19)
    box4 = BoundingBox(979, Rectangle(0.22, 0.34, 0.62, 0.85), "horse", 0.8, object_id=100)

    bounding_boxes_object = BoundingBoxes([box2, box3, box4], '13')
    bounding_boxes_object2 = BoundingBoxes([box1], '12')

    return {bounding_boxes_object.image_id: bounding_boxes_object,
            bounding_boxes_object2.image_id: bounding_boxes_object2}



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
    return get_small_frame()


@pytest.fixture
def large_frame():
    """Fixture that gets a big frame loaded with opencv.

    Returns:
        np.ndarray: Opencv frame from test data.
    """
    __image_name = f'{root_path}/data/tests/unittests/big_image.jpg'
    return get_large_frame()


def get_small_frame():
    """Fixture for a small frame loaded with opencv.

    Returns:
        np.ndarray: Opencv frame from test data.
    """
    __image_name = f'{root_path}/data/tests/unittests/small_image.jpg'
    return cv2.imread(__image_name)


def get_large_frame():
    """Fixture that gets a big frame loaded with opencv.

    Returns:
        np.ndarray: Opencv frame from test data.
    """
    __image_name = f'{root_path}/data/tests/unittests/big_image.jpg'
    return cv2.imread(__image_name)
