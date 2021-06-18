"""Tests BoxesMessage by checking properties and internal behavior.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from processor.websocket.boxes_message import BoxesMessage
from processor.data_object.rectangle import Rectangle
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.utils.text import bounding_boxes_to_dict


# pylint: disable=attribute-defined-outside-init,no-member
class TestBoxesMessage:
    """Testing BoxesMessage.

    Attributes:
        data (BoxesMessage): Example BoxesMessage.
        frame_id (int): Frame identifier.
        empty_bounding_boxes (BoundingBoxes): Empty bounding boxes object.
        bounding_boxes (BoundingBoxes): BoundingBoxes object with a single bounding box.
        example_boxes_msg (dict): Example dictionary from bounding boxes.
    """

    def setup_method(self):
        """Setup method."""
        self.frame_id = 1.0
        self.empty_bounding_boxes = BoundingBoxes([])
        bounding_box = BoundingBox(1, Rectangle(.1, .2, .3, .4), 'car', 0.5)
        self.bounding_boxes = BoundingBoxes([bounding_box])
        self.example_boxes_msg = {'type': 'boundingBoxes',
                                  'frameId': self.frame_id,
                                  'boxes': BoundingBoxes([bounding_box])}
        self.data = BoxesMessage(self.frame_id, self.bounding_boxes)

    def test_init(self):
        """Tests initialize properties set of UpdateMessage."""
        assert self.data.frame_id == self.frame_id
        assert self.data.bounding_boxes == self.bounding_boxes

    def test_invalid_init(self):
        """Tests whether type is enforced correctly by the constructor."""
        with pytest.raises(TypeError):
            BoxesMessage(1, self.empty_bounding_boxes)
        with pytest.raises(TypeError):
            BoxesMessage('invalid', self.empty_bounding_boxes)
        with pytest.raises(TypeError):
            BoxesMessage(1.0, [])

    def test_invalid_from_message(self):
        """Tests whether a message with missing keys raises Exceptions."""
        # Create invalid messages.
        missing_frame_id_msg = self.example_boxes_msg.copy()
        missing_frame_id_msg.pop('frameId')

        missing_boxes_msg = self.example_boxes_msg.copy()
        missing_boxes_msg.pop('boxes')

        # Test whether from_message raises exception with invalid messages.
        with pytest.raises(KeyError):
            BoxesMessage.from_message(missing_frame_id_msg)

        with pytest.raises(KeyError):
            BoxesMessage.from_message(missing_boxes_msg)

    def test_eq(self):
        """Tests eq function."""
        # Creates another UpdateMessage and checks whether they are equal.
        self.other = BoxesMessage(self.frame_id, self.bounding_boxes)
        assert self.data == self.other

        # Also asserts that unequal objects are detected correctly.
        assert self.data != BoxesMessage(self.frame_id + 1, self.bounding_boxes)
        assert self.data != BoxesMessage(self.frame_id, self.empty_bounding_boxes)

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.data).startswith('BoxesMessage(')

    def test_message_parsing(self):
        """Tests that a BoxesMessage constructed from a message can be converted into the original message.

        This method tests both the from_message and to_message functionality of the class.
        """
        message = BoxesMessage.from_message(self.example_boxes_msg)
        expected = bounding_boxes_to_dict(self.bounding_boxes, self.frame_id)
        assert message.to_message() == expected


if __name__ == '__main__':
    pytest.main(TestBoxesMessage)
