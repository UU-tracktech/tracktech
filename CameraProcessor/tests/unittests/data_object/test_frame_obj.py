"""Tests frame object by checking properties and whether drawing changes something

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import json
import pytest
import cv2
import numpy
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.frame_obj import FrameObj
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


class TestFrameObj:
    """Tests FrameObj."""

    def setup_method(self):
        """Setup method."""
        self.data = FrameObj(get_sample_frame(), 1)
        self.frame = self.data.get_frame()
        self.timestamp = self.data.get_timestamp()
        self.shape = self.data.get_shape()

    def test_value_frame_obj(self):
        """Asserts if value of frame is correct.

        """
        assert is_same_frame_image(get_sample_frame(), self.data.get_frame())

    def test_frame(self):
        """Asserts if frame is correct"""
        assert1 = FrameObj(get_sample_frame(), 1).get_frame()
        assert2 = self.frame
        assert len(assert1) == len(assert2)
        assert numpy.testing.assert_array_equal(assert1, assert2) is None

    def test_timestamp(self):
        """Asserts if frame is correct"""
        assert FrameObj(get_sample_frame(), 1).get_timestamp() == self.timestamp

    def test_shape(self):
        """Asserts if frame is correct"""
        assert FrameObj(get_sample_frame(), 1).get_shape() == self.shape


if __name__ == '__main__':
    pytest.main(TestFrameObj)