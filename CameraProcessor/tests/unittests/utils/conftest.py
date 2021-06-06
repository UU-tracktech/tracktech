"""Fixtures and configurations available to utils tests.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.utils.draw import draw_tracking_boxes, draw_detection_boxes

X0, X1 = 60, 120
Y0, Y1 = 120, 180
IMG_SIZE = 200


@pytest.fixture
def bbox():
    """Fixture for an example bounding box.

    Returns:
        BoundingBox: A boundingbox for use in testing.
    """
    # Create a dummy bounding box.
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
    """Fixture for the function, text, and seed.

    Args:
        request ([object]): List of parameters for the fixture
    """
    return request.param
