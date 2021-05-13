"""Tests main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest

from processor.pipeline.tracking.itracker import ITracker
from processor.data_object.frame_obj import FrameObj
from processor.data_object.bounding_boxes import BoundingBoxes


class TestITracker(ITracker):

    def test_itracker_error(self):
        with pytest.raises(NotImplementedError):
            ITracker.track(self, BoundingBoxes, FrameObj)


if __name__ == '__main__':
    pytest.main(TestITracker)
