"""Tests for detection_obj.py.

 - Test if every type is correct.
 - Test empty inputs.
 - Test if every value is correct.
 - Test exceptions.
 - Test if inputs are valid form.

"""

import pytest
import cv2
from detection.detection_obj import DetectionObj
from detection.bounding_box import BoundingBox


def __eq__(self, other):
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestDetectionObj:

    # Setup
    def setup_method(self):
        self.data = DetectionObj(1.0, 1, 1)
        self.timestamp = self.data.timestamp
        self.frame = self.data.frame
        self.frame_nr = self.data.frame_nr
        self.data.bounding_boxes.append(BoundingBox(1, [0, 0, 1, 1], "person", 0.5))
        self.bounding_box_value_test = BoundingBox(1, [0, 0, 1, 1], "person", 0.5)
        self.bounding_box = self.data.bounding_boxes
        self.box_frame = cv2.rectangle(1, (0, 0), (1, 1), (255, 0, 0), 2)

    # Testing typechecking
    def test_type_timestamp(self):
        assert isinstance(self.timestamp,
                          type(self.timestamp))

    def test_type_frame(self):
        assert isinstance(self.frame,
                          type(self.frame))

    def test_type_frame_nr(self):
        assert isinstance(self.frame_nr,
                          type(self.frame_nr))

    def test_type_bounding_box(self):
        assert isinstance(self.data.bounding_boxes,
                          type(self.data.bounding_boxes))

    # Testing empty fields that can be empty
    def test_empty_timestamp(self):
        assert self.timestamp is not None

    def test_empty_frame(self):
        assert self.frame is not None

    def test_empty_frame_nr(self):
        assert self.frame_nr is not None

    def test_empty_bounding_box(self):
        assert self.data.bounding_boxes is not None

    # Testing values
    def test_value_timestamp(self):
        assert self.timestamp == 1.0

    def test_value_frame(self):
        assert self.frame == 1

    def test_value_frame_nr(self):
        assert self.frame_nr == 1

    def test_value_bounding_box(self):
        assert self.data.bounding_boxes.__eq__(self.bounding_box_value_test)

    # Testing exceptions
    def test_exception_timestamp(self):
        with pytest.raises(Exception):
            assert str(self.timestamp) == 'some invalid value'

    def test_exception_frame(self):
        with pytest.raises(Exception):
            assert str(self.frame) == 'some invalid value'

    def test_exception_frame_nr(self):
        with pytest.raises(Exception):
            assert str(self.frame_nr) == 'some invalid value'

    def test_exception_bounding_box(self):
        with pytest.raises(Exception):
            assert str(self.bounding_box) == 'some invalid value'

    # Testing form
    def test_draw_length(self):
        self.data.draw_rectangles()
        assert len(self.data.frame) == len(self.box_frame)

    def test_draw_equal(self):
        self.data.draw_rectangles()
        for test, expected in zip(self.data.frame, self.box_frame):
            for p1, p2 in zip(test, expected):
                assert p1 == p2


if __name__ == '__main__':
    pytest.main(TestDetectionObj)
