"""Testing files for process frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from collections import OrderedDict
import numpy as np

from tests.unittests.conftest import get_small_frame
from tests.unittests.conftest import get_large_frame
from tests.unittests.utils.utils import get_sample_frame
from processor.pipeline.frame_buffer import FrameBuffer
from processor.data_object.rectangle import Rectangle
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.frame_obj import FrameObj


# pylint: disable=attribute-defined-outside-init
class TestFrameBuffer:
    """Test frame_buffer.py.

    Attributes:
        frame_buffer (BoundingBoxes): Bounding boxes object to test.
        box1 (BoundingBox): A sample bounding box.
        box2 (BoundingBox): A sample bounding box.
        boxes1 (BoundingBoxes): Bounding boxes object to test.
        frame1 (FrameObj): A sample frame.
        box3 (BoundingBox): A sample bounding box.
        boxes2 (BoundingBoxes): Bounding boxes object to test.
        frame2 (FrameObj):  A sample frame.
    """

    def setup_method(self):
        """Sets up FrameBuffer for unit testing."""

        self.frame_buffer = FrameBuffer(2)

        # Create sample bounding boxes and frame objects.
        self.box1 = BoundingBox(1, Rectangle(0, 0.5, 0.75, 1), 'person', 0.5, object_id=5)
        self.box2 = BoundingBox(2, Rectangle(0.1, 0.25, 0.5, 0.9), 'car', 0.75, object_id=7)
        self.boxes1 = BoundingBoxes([self.box1, self.box2], 'test_1')
        self.frame1 = FrameObj(get_small_frame(), 1)

        self.box3 = BoundingBox(3, Rectangle(0.2, 0.6, 0.4, 0.7), 'person', 0.65, object_id=10)
        self.boxes2 = BoundingBoxes([self.box3], 'test_2')
        self.frame2 = FrameObj(get_large_frame(), 3)

        # Add the sample bounding boxes and frame objects to the frame buffer.
        self.frame_buffer.add_frame(self.frame1, self.boxes1)
        self.frame_buffer.add_frame(self.frame2, self.boxes2)

    def test_get_frame(self):
        """Test whether the frame_buffer contains the frame objects."""
        assert np.all(self.frame_buffer.get_frame(self.frame1.timestamp) == self.frame1)
        assert np.all(self.frame_buffer.get_frame(self.frame2.timestamp) == self.frame2)

    def test_get_boxes(self):
        """Test whether the frame_buffer contains the correct BoundingBoxes given a frame id."""
        assert self.frame_buffer.get_boxes(self.frame1.timestamp) == self.boxes1
        assert self.frame_buffer.get_boxes(self.frame2.timestamp) == self.boxes2

    def test_get_box(self):
        """Test whether the frame_buffer contains the correct BoundingBox given a frame id and a box id."""
        assert self.frame_buffer.get_box(self.frame1.timestamp, self.box1.identifier) == self.box1
        assert self.frame_buffer.get_box(self.frame1.timestamp, self.box2.identifier) == self.box2
        assert self.frame_buffer.get_box(self.frame2.timestamp, self.box3.identifier) == self.box3

    def test_buffer(self):
        """Test the buffer property of frame_buffer."""
        ordered_dict = OrderedDict()
        ordered_dict[self.frame1.timestamp] = (self.frame1, self.boxes1)
        ordered_dict[self.frame2.timestamp] = (self.frame2, self.boxes2)

        assert self.frame_buffer.buffer == ordered_dict

    def test_delete_item_in_buffer(self):
        """Test that the frame_buffer will delete the oldest item, when the buffer size overflows."""
        box4 = BoundingBox(4, Rectangle(0.3, 0.41, 0.45, 0.6), 'person', 0.75, object_id=20)
        boxes3 = BoundingBoxes([box4], 'test_3')
        frame3 = FrameObj(get_sample_frame(), 5)
        self.frame_buffer.add_frame(frame3, boxes3)

        assert len(self.frame_buffer.buffer) == 2
        assert frame3.timestamp in self.frame_buffer.buffer
        assert self.frame2.timestamp in self.frame_buffer.buffer
        assert self.frame1.timestamp not in self.frame_buffer.buffer
