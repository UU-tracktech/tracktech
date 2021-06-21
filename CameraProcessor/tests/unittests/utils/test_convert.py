"""Tests convert functions.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.unittests.utils.utils import get_sample_frame
from processor.data_object.frame_obj import FrameObj
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.utils.convert import to_buffer_dict


# pylint: disable=attribute-defined-outside-init,no-member
class TestConvert:
    """Tests the convert function."""

    def setup_method(self):
        """Setup method."""
        self.frame_obj = FrameObj(get_sample_frame(), 12)
        self.box1 = [BoundingBox(1, Rectangle(0, 0, 1, 1), 'person', 0.5)]
        self.dict1 = to_buffer_dict(self.frame_obj, self.box1)

    def test_convert(self):
        """Tests the to_buffer_dict function."""
        expected_dict = {
            'frame': self.frame_obj.frame,
            'frameId': self.frame_obj.timestamp,
            'boxes': [
                {
                    'boxId': bounding_box.identifier,
                    'rect': bounding_box.rectangle
                }
                for bounding_box in BoundingBoxes(self.box1)
            ]
        }

        assert expected_dict == self.dict1
        assert self.dict1['frameId'] == 12
        assert len(self.dict1['frame']) > 0


if __name__ == '__main__':
    pytest.main(TestConvert)
