"""Tests frame object by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
import numpy

from tests.unittests.utils.utils import get_sample_frame
from processor.data_object.frame_obj import FrameObj


# pylint: disable=attribute-defined-outside-init,no-member
class TestFrameObj:
    """Tests frame_obj.py.

    Attributes:
        frame1 (FrameObj): sample frame for texting.
        frame2 (FrameObj): sample frame for texting.
        frame (numpy.ndarray): the frame from the capture given by OpenCV.
        timestamp (float): timestamp (in s) associated with the current frame.
        shape (int, int): width and height of frame.
    """

    def setup_method(self):
        """Sets up frame_object for unit testing."""
        self.frame1 = FrameObj(get_sample_frame(), 1337)
        self.frame2 = FrameObj(get_sample_frame(), 7331)
        self.frame = get_sample_frame()
        self.timestamp = 1337
        self.shape = 640, 480

    def test_init(self):
        """Tests the constructor of the FrameObj object."""
        assert numpy.all(self.frame == self.frame1.frame)
        assert self.timestamp == self.frame1.timestamp
        assert self.shape == self.frame1.shape

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.frame1).startswith('FrameObj(')


if __name__ == '__main__':
    pytest.main(TestFrameObj)
