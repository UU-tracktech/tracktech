import pytest
import os
import json
import cv2
from processor.pipeline.detection.bounding_box import BoundingBox
from processor.pipeline.detection.detection_obj import DetectionObj
from tests.unittests.utils.utils import get_sample_frame, is_same_frame_image


# pylint: disable=attribute-defined-outside-init, no-member
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


class TestDetectionObj:
    """Tests detection_obj.py.

    """

    # Setup
    def setup_method(self):
        """Set ups detection_obj for unit testing.

        """
        self.original_frame = get_sample_frame()
        self.data = DetectionObj(1.0, get_sample_frame(), 1)
        self.timestamp = self.data.timestamp
        self.frame = self.data.frame
        self.frame_nr = self.data.frame_nr
        self.data.bounding_boxes.append(BoundingBox(1, [0, 0, 1, 1], "person", 0.5))
        self.bounding_box_value_test = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.bounding_box = self.data.bounding_boxes
        self.box_frame = cv2.rectangle(1, (0, 0), (1, 1), (255, 0, 0), 2)

    # Testing typechecking
    def test_type_timestamp(self):
        """Asserts if value of timestamp is of correct type.

        """
        assert isinstance(self.timestamp,
                          type(self.timestamp))

    def test_type_frame(self):
        """Asserts if value of frame is of correct type.

        """
        assert isinstance(self.frame,
                          type(self.frame))

    def test_type_frame_nr(self):
        """Asserts if value of frame_nr is of correct type.

        """
        assert isinstance(self.frame_nr,
                          type(self.frame_nr))

    def test_type_bounding_boxes(self):
        """Asserts if value of bounding_boxes is of correct type.

        """
        assert isinstance(self.data.bounding_boxes,
                          type(self.data.bounding_boxes))

    # Testing empty fields that can be empty
    def test_empty_timestamp(self):
        """Asserts if timestamp is not None.

        """
        assert self.timestamp is not None

    def test_empty_frame(self):
        """Asserts if frame is not None.

        """
        assert self.frame is not None

    def test_empty_frame_nr(self):
        """Asserts if frame_nr is not None.

        """
        assert self.frame_nr is not None

    def test_empty_bounding_boxes(self):
        """Asserts if bounding_boxes is not None.

        """
        assert self.data.bounding_boxes is not None

    # Testing exceptions
    def test_exception_timestamp(self):
        """Asserts if timestamp throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.timestamp) == 'some invalid value'

    def test_exception_frame(self):
        """Asserts if frame throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.frame) == 'some invalid value'

    def test_exception_frame_nr(self):
        """Asserts if frame_nr throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.frame_nr) == 'some invalid value'

    def test_exception_bounding_boxes(self):
        """Asserts if bounding_boxes throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.bounding_box) == 'some invalid value'\


    # Testing values
    def test_value_timestamp(self):
        """Asserts if value of timestamp is correct.

        """
        assert self.timestamp == 1.0

    def test_value_frame(self):
        """Asserts if value of frame is correct.

        """
        assert is_same_frame_image(self.original_frame, self.data.frame)

    def test_value_frame_nr(self):
        """Asserts if value of frame_nr is correct.

        """
        assert self.frame_nr == 1

    def test_value_bounding_boxes(self):
        """Asserts if value of bounding_box is correct.

        """
        assert self.data.bounding_boxes.__eq__(self.bounding_box_value_test)

    # Testing form
    def test_draw_changes_frame(self):
        """Asserts that the draw rectangles actually draws something on the screen

        """
        assert is_same_frame_image(self.original_frame, self.data.frame)
        self.data.draw_rectangles()
        assert not is_same_frame_image(self.original_frame, self.data.frame)

    def test_to_json(self):
        """Asserts if the to_json() method works properly

        """
        assert self.data.to_json() == json.dumps({
            "type": "boundingBoxes",
            "frameId": self.timestamp,
            "boxes": [bbox.to_dict() for bbox in self.bounding_box]
        })

if __name__ == '__main__':
    pytest.main(TestDetectionObj)
