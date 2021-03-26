"""Tests for detection_obj.py.

test

"""


import pytest
from detection.detection_obj import DetectionObj


class TestDetectionObject:

    def setup_method(self):
        self.init = DetectionObj(1.0, 1, 1)
        self.timestamp = self.init.timestamp
        self.frame = self.init.frame
        self.frame_nr = self.init.frame_nr
        self.bounding_box = self.init.bounding_box


if __name__ == '__main__':
    pytest.main()
