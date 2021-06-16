"""Tests the bounding box object.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init
class TestBoundingBoxes:
    """Tests bounding_boxes.py.

    Attributes:
        box1 (BoundingBox): A sample bounding box.
        box1_duplicate (BoundingBox): Duplicate of box1 without a reference.
        box2 (BoundingBox): A sample bounding box.
        boxes_id (str): Identifier of the BoundingBoxes object.
        boxes (BoundingBoxes): Bounding boxes object to test.
        boxes_duplicate (BoundingBoxes): Bounding boxes object to test.
        boxes_eq (BoundingBoxes): Bounding boxes object to test.
    """

    def setup_method(self):
        """Sets up BoundingBoxes for unit testing."""
        self.box1 = BoundingBox(1, Rectangle(0, 0, 1, 1), 'person', 0.5)
        self.box1_duplicate = BoundingBox(1, Rectangle(0, 0, 1, 1), 'person', 0.5)
        self.box2 = BoundingBox(2, Rectangle(0, 0, 1, 1), 'person', 0.5)
        self.boxes_id = 'test'

        self.boxes = BoundingBoxes([self.box1, self.box2], self.boxes_id)
        self.boxes_duplicate = BoundingBoxes([self.box1_duplicate, self.box2], self.boxes_id)
        self.boxes_eq = BoundingBoxes([self.box2, self.box1], self.boxes_id)

    def test_init(self):
        """Tests the constructor of the BoundingBoxes object."""
        assert self.boxes.image_id == self.boxes_id

        boxes_list = self.boxes.bounding_boxes
        assert boxes_list[0] == self.box1
        assert boxes_list[1] == self.box2

    def test_len(self):
        """Asserts if value of frame is of correct type."""
        assert len(self.boxes) == 2
        assert len(BoundingBoxes([], '')) == 0

    def test_iter(self):
        """Tests whether the iterator works for BoundingBoxes."""
        for box in self.boxes:
            assert box in (self.box1, self.box2)

    def test_eq(self):
        """Tests whether checking equality works."""
        assert self.boxes == self.boxes_duplicate
        assert self.boxes != self.boxes_eq

    def test_repr(self):
        """Tests that the string version contains."""
        assert str(self.boxes).startswith('BoundingBoxes(')


if __name__ == '__main__':
    pytest.main(TestBoundingBoxes)
