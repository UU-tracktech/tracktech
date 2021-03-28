import pytest
from tracking.tracking_obj import TrackingObj
from detection.detection_obj import DetectionObj
from detection.bounding_box import BoundingBox


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


class TestTrackingObj:
    """Tests tracking_obj.py.

    """

    # Setup
    def setup_method(self):
        """Set ups tracking_obj for unit testing.

        """
        self.data = TrackingObj(DetectionObj(1.0, 1, 1), [])
        self.frame = self.data.frame
        self.frame_nr = self.data.frame_nr
        self.tracking_feature_maps = self.data.tracking_feature_maps
        self.data.bounding_boxes.append(BoundingBox(1, [0, 0, 1, 1], "person", 0.5))
        self.data.tracked_boxes.append(BoundingBox(1, [0, 0, 1, 1], "person", 0.5))

    # Testing typechecking
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

    def test_type_tracking_feature_map(self):
        """Asserts if value of tracking_feature_map is of correct type.

        """
        assert isinstance(self.tracking_feature_maps,
                          type(self.tracking_feature_maps))

    def test_type_bounding_boxes(self):
        """Asserts if value of bounding_boxes is of correct type.

        """
        assert isinstance(self.data.bounding_boxes,
                          type(self.data.bounding_boxes))

    def test_type_tracked_boxes(self):
        """Asserts if value of tracked_boxes is of correct type.

        """
        assert isinstance(self.data.tracked_boxes,
                          type(self.data.tracked_boxes))

    # Testing empty fields that can be empty
    def test_empty_frame(self):
        """Asserts if frame is not None.

        """
        assert self.frame is not None

    def test_empty_frame_nr(self):
        """Asserts if frame_nr is not None.

        """
        assert self.frame_nr is not None

    def test_empty_tracking_feature_maps(self):
        """Asserts if tracking_feature_maps is not None.

        """
        assert self.tracking_feature_maps is not None

    def test_empty_bounding_boxes(self):
        """Asserts if bounding_boxes is not None.

        """
        assert self.data.bounding_boxes is not None

    def test_empty_tracked_boxes(self):
        """Asserts if tracked_boxes is not None.

        """
        assert self.data.tracked_boxes is not None

    # Testing exceptions
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

    def test_exception_tracking_feature_maps(self):
        """Asserts if tracking_feature_maps throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.tracking_feature_maps) == 'some invalid value'

    def test_exception_bounding_boxes(self):
        """Asserts if bounding__boxes throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.data.bounding_boxes) == 'some invalid value'

    def test_exception_tracked_boxes(self):
        """Asserts if tracked_boxes throws exception.

        """
        with pytest.raises(Exception):
            assert str(self.data.tracked_boxes) == 'some invalid value'


if __name__ == '__main__':
    pytest.main(TestTrackingObj)
