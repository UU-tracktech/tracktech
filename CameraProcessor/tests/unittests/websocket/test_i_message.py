"""Tests IMessage by checking whether NotIMplemented exceptions are raised.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from processor.websocket.i_message import IMessage


# pylint: disable=attribute-defined-outside-init,no-member
class TestIMessage:
    """Tests i_message.py.

    Attributes:
        i_message (IMessage): IMessage object used for texting.
    """

    def setup_method(self):
        """Sets up IMessage for unit testing."""
        self.i_message = IMessage()

    def test_raises_not_implemented(self):
        """Tests that NotImplementedExceptions are raised."""
        with pytest.raises(NotImplementedError):
            self.i_message.to_message()

        with pytest.raises(NotImplementedError):
            IMessage.from_message('')


if __name__ == '__main__':
    pytest.main(TestIMessage)
