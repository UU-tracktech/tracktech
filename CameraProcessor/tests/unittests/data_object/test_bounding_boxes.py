"""Tests detection object by checking properties and whether drawing changes something

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import json
import pytest
import cv2
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from tests.unittests.utils.utils import get_sample_frame, is_same_frame_image
from processor.data_object.rectangle import Rectangle
from processor.utils.draw import draw_bounding_boxes


# pylint: disable=attribute-defined-outside-init,no-member
def __eq__(self, other):
    """Custom equalize function

    Args:
        self: first object to compare
        other: second object to compare

    Returns: bool

    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestBoundingBoxes:
    """Tests bounding_boxes.py.

    """

    # Setup
    def setup_method(self):
        """Set ups detection_obj for unit testing.

        """
        self.original_frame = get_sample_frame()
        self.box1 = BoundingBox(1, Rectangle(0, 0, 1, 1), "person", 0.5)
        self.box2 = BoundingBox(2, Rectangle(0, 0, 1, 1), "person", 0.5)
        self.data = BoundingBoxes([self.box1, self.box2])
        self.boxes = self.data.get_bounding_boxes()
        self.frame = self.box1.get_identifier()
        self.bounding_box_value_test = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.box_frame = cv2.rectangle(1, (0, 0), (1, 1), (255, 0, 0), 2)

    # Testing typechecking
    def test_type_timestamp(self):
        """Asserts if value of timestamp is of correct type.

        """
        assert isinstance(self.frame,
                          type(self.frame))

    def test_type_frame(self):
        """Asserts if value of frame is of correct type.

        """
        assert isinstance(self.frame,
                          type(self.frame))

    # Testing empty fields that can be empty
    def test_empty_frame(self):
        """Asserts if frame is not None.

        """
        assert self.frame is not None

    # Testing exceptions
    def test_exception_frame(self):
        """Asserts if frame throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.frame) == 'some invalid value'

    def test_exception_bounding_boxes(self):
        """Asserts if bounding_boxes throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.data.get_bounding_boxes()) == 'some invalid value'


if __name__ == '__main__':
    pytest.main(TestBoundingBoxes)
