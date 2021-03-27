import pytest
from tracking.tracking_obj import TrackingObj
from detection.detection_obj import DetectionObj
from detection.bounding_box import BoundingBox


def __eq__(self, other):
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False


class TestTrackingObj:

    # Setup
    def setup_method(self):
        self.data = TrackingObj(DetectionObj(1.0, 1, 1), [])
        self.frame = self.data.frame
        self.frame_nr = self.data.frame_nr
        self.tracking_feature_maps = self.data.tracking_feature_maps
        self.bounding_boxes = self.data.bounding_boxes.append(BoundingBox(1, [0, 0, 1, 1], "person", 0.5))
        self.tracked_boxes = self.data.tracked_boxes


if __name__ == '__main__':
    pytest.main(TestTrackingObj)
