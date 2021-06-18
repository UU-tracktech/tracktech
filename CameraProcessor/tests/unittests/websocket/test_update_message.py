"""Tests UpdateMessage by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from processor.websocket.update_message import UpdateMessage


# pylint: disable=attribute-defined-outside-init,no-member
class TestUpdateMessage:
    """Testing UpdateMessage.

    Attributes:
        data (UpdateMessage): Example UpdateMessage.
        example_feature_map ([float]): A small example featuremap.
        example_update_msg (dict): An example json message.
        object_id (int): Object identifier.
    """
    def setup_method(self):
        """Setup method."""
        self.object_id = 1
        self.example_feature_map = [0.1, 0.2, 0.3]
        self.example_update_msg = {'type': 'featureMap', 'objectId': 2, 'featureMap': [0.4]}
        self.data = UpdateMessage(self.object_id, self.example_feature_map)

    def test_init(self):
        """Tests initialize properties set of UpdateMessage."""
        assert self.data.object_id == self.object_id
        assert self.data.feature_map == [0.1, 0.2, 0.3]

    def test_invalid_init(self):
        """Tests whether type is enforced correctly by the constructor."""
        with pytest.raises(TypeError):
            UpdateMessage(.1, [1.])
        with pytest.raises(TypeError):
            UpdateMessage("inv", [1.])
        with pytest.raises(TypeError):
            UpdateMessage(1, ['not a float'])
        with pytest.raises(AttributeError):
            UpdateMessage(1, [])

    def test_invalid_from_message(self):
        """Tests whether a message with missing keys raises Exceptions."""
        # Create invalid messages.
        missing_feature_map_msg = self.example_update_msg.copy()
        missing_feature_map_msg.pop('featureMap')

        missing_object_id_msg = self.example_update_msg.copy()
        missing_object_id_msg.pop('objectId')

        # Test whether from_message raises exception with invalid messages.
        with pytest.raises(KeyError):
            UpdateMessage.from_message(missing_feature_map_msg)

        with pytest.raises(KeyError):
            UpdateMessage.from_message(missing_object_id_msg)

    def test_eq(self):
        """Tests eq function."""
        # Creates another UpdateMessage and checks whether they are equal.
        self.other = UpdateMessage(self.object_id, self.example_feature_map)
        assert self.data == self.other

        # Also asserts that unequal objects are detected correctly.
        assert self.data != UpdateMessage(self.object_id + 1, self.example_feature_map)
        assert self.data != UpdateMessage(self.object_id, self.example_feature_map + [.1])

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.data).startswith('UpdateMessage(')

    def test_message_parsing(self):
        """Tests that a UpdateMessage constructed from a message can be converted into the original message.

        This method tests both the from_message and to_message functionality of the class.
        """
        message = UpdateMessage.from_message(self.example_update_msg)
        assert message.to_message() == self.example_update_msg


if __name__ == '__main__':
    pytest.main(TestUpdateMessage)
