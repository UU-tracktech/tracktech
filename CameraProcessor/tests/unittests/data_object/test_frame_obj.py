"""Tests frame object by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
import numpy

from processor.data_object.frame_obj import FrameObj
from tests.unittests.utils.utils import get_sample_frame, is_same_frame_image


# pylint: disable=attribute-defined-outside-init,no-member
def __eq__(self, other):
    """Custom equalize function for a FrameObj.

    Args:
        other (FrameObj): second object to compare to.

    Returns:
        bool: Whether the frame objects are the same
    """
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestFrameObj:
    """Tests FrameObj properties.

    Attributes:
        data (FrameObj): Frame object containing an example frame.
        frame (numpy.ndarray): Frame in a numpy array.
        timestamp (float): Timestamp of the frame.
        shape (width, height): Shape of the frame
    """

    def setup_method(self):
        """Setup method."""
        self.data = FrameObj(get_sample_frame(), 1)
        self.frame = self.data.get_frame()
        self.timestamp = self.data.get_timestamp()
        self.shape = self.data.get_shape()

    def test_value_frame_obj(self):
        """Asserts if value of frame is correct."""
        assert is_same_frame_image(get_sample_frame(), self.data.get_frame())

    def test_frame(self):
        """Asserts if frame is correct."""
        assert1 = FrameObj(get_sample_frame(), 1).get_frame()
        assert2 = self.frame

        # Frame is equal to the set.
        assert len(assert1) == len(assert2)
        assert numpy.testing.assert_array_equal(assert1, assert2) is None

    def test_timestamp(self):
        """Asserts if frame timestamp is correct."""
        assert FrameObj(get_sample_frame(), 1).get_timestamp() == self.timestamp

    def test_shape(self):
        """Asserts if frame shape is correct."""
        assert FrameObj(get_sample_frame(), 1).get_shape() == self.shape


if __name__ == '__main__':
    pytest.main(TestFrameObj)
