"""Tests for detection_obj.py.

test

"""

import pytest
import cv2
from detection.detection_obj import DetectionObj


class TestDetectionObj:

    # Setup
    def setup_method(self):
        self.data = DetectionObj(1.0, 1, 1)
        self.timestamp = self.data.timestamp
        self.frame = self.data.frame
        self.frame_nr = self.data.frame_nr
        self.data.bounding_box = [[0, 0, 1, 1]]
        self.bounding_box = self.data.bounding_box
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
        assert isinstance(self.bounding_box,
                          type(self.bounding_box))

    # Testing empty fields that can be empty
    def test_empty_timestamp(self):
        assert self.timestamp is not None

    def test_empty_frame(self):
        assert self.frame is not None

    def test_empty_frame_nr(self):
        assert self.frame_nr is not None

    def test_empty_bounding_box(self):
        assert self.bounding_box is not None

    # Testing drawing function
    @pytest.mark.skip(reason="Not testable right now")
    def test_draw_equal(self):
        assert self.data.draw_rectangles() == self.box_frame


if __name__ == '__main__':
    pytest.main(TestDetectionObj)
