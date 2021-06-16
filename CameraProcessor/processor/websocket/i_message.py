"""Contains an interface for a message to be sent or received by the websocket.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class IMessage:
    """Interface class for messages to sent or received via the websocket."""

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a message class instantiation."""
        raise NotImplementedError("Expected function from_message not implemented.")

    def to_message(self):
        """Converts a message object to a dict representation."""
        raise NotImplementedError("Expected function to_message not implemented.")
