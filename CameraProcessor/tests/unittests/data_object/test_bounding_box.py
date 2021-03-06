"""Tests the bounding box by creating one and testing the properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init
class TestBoundingBox:
    """Tests bounding_box.py.

    Attributes:
        box1 (BoundingBox): A sample bounding box.
        box1_duplicate (BoundingBox): Duplicate of box1 without a reference.
        box2 (BoundingBox): A sample bounding box.
        identifier (int): identifier of bounding box.
        rectangle (Rectangle): coords of bounding box, contains bottom left and top right coords.
        classification (str): classification of the bounding box.
        certainty (float): certainty/confidence of the bounding box detection.
        object_id (int): id assigned to object depicted by the bounding box.
    """

    def setup_method(self):
        """Sets up bounding_box for unit testing."""
        self.box1 = BoundingBox(1, Rectangle(0, 0.5, 0.75, 1), 'person', 0.5, object_id=5)
        self.box1_duplicate = BoundingBox(1, Rectangle(0, 0.5, 0.75, 1), 'person', 0.5, object_id=5)
        self.box2 = BoundingBox(1, Rectangle(0.1, 0.25, 0.5, 0.9), 'car', 0.75, object_id=15)
        self.identifier = 1
        self.rectangle = Rectangle(0, 0.5, 0.75, 1)
        self.classification = 'person'
        self.certainty = 0.5
        self.object_id = 5

    def test_init(self):
        """Tests the constructor of the BoundingBox object."""
        assert self.identifier == self.box1.identifier
        assert self.rectangle == self.box1.rectangle
        assert self.classification == self.box1.classification
        assert self.object_id == self.box1.object_id

    def test_eq(self):
        """Tests the __eq__ function."""
        assert self.box1 != self.box2
        assert self.box1 == self.box1_duplicate

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.box1).startswith('BoundingBox(')


if __name__ == '__main__':
    pytest.main(TestBoundingBox)
