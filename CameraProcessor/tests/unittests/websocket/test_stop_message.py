"""Tests StopMessage by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest
from processor.websocket.stop_message import StopMessage


# pylint: disable=attribute-defined-outside-init,no-member
class TestStopMessage:
    """Testing StopMessage.

    Attributes:
        data (StopMessage): Example StopMessage.
        other (StopMessage): Other StopMessage.
        object_id (int): Object identifier.
    """
    def setup_method(self):
        """Setup method."""
        self.object_id = 1
        self.data = StopMessage(self.object_id)

    def test_init(self):
        """Tests init."""
        assert self.data.object_id == self.object_id

    def test_invalid_init(self):
        """Tests whether an error is raised when the values in the StopMessage are invalid."""
        with pytest.raises(TypeError):
            StopMessage(1.)  # Test with float rather than int.
        with pytest.raises(TypeError):
            StopMessage("1")  # Test with string rather than int.

    def test_invalid_from_message(self):
        """Tests whether a message with missing keys raises Exceptions."""
        # Create invalid messages.
        missing_stop_message = {'type': 'stop'}

        # Test whether from_message raises exception with invalid messages.
        with pytest.raises(KeyError):
            StopMessage.from_message(missing_stop_message)

    def test_eq(self):
        """Tests eq function."""
        self.other = StopMessage(self.object_id)
        assert self.data == self.other

        # To make sure it also detects when message is not the same.
        assert self.data != StopMessage(self.object_id + 1)

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.data).startswith('StopMessage(')

    def test_message_parsing(self):
        """Tests that a StopMessage constructed from a  message can be converted into the original message.

        This method tests both the from_message and to_message functionality of the class.
        """
        dict_message = {'type': 'stop', 'objectId': self.object_id}
        message = StopMessage.from_message(dict_message)
        assert message.to_message() == dict_message


if __name__ == '__main__':
    pytest.main(TestStopMessage)
