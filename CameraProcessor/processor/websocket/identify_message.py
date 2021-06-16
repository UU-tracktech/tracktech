"""Contains IdentifyMessage class which contains an identifier for the processor to the orchestrator.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.websocket.i_message import IMessage


class IdentifyMessage(IMessage):
    """Send-only command that holds an identifier for the processor."""
    def __init__(self, identifier):
        """Constructor for the IdentifyMessage class.

        Args:
            identifier (string): identifier of the camera processor.
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier should be a string")

        self.__identifier = identifier

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a IdentifyCommand.

        Args:
            message (dict): Python dict representation of an incoming JSON message.

        Returns:
            (IdentifyMessage): IdentifyCommand constructed from the dict.
        """
        if "id" not in message.keys():
            raise KeyError("id missing")

        identifier = message["id"]

        return IdentifyMessage(identifier)

    def to_message(self):
        """Converts the IdentifyMessage to a dict representation.

        Returns:
            (dict): Python dict representation of the message.
        """
        return {
            "type": "identifier",
            "id": self.__identifier
        }

    @property
    def identifier(self):
        """Get identifier.

        Returns:
            (str): Identifier of the camera processor.
        """
        return self.__identifier

    def __eq__(self, other):
        """Function that checks whether the current IdentifyCommand is the same as the given one.

        Args:
            other (IdentifyMessage): IdentifyCommand to compare with.

        Returns:
            bool: Whether the messages are the same.
        """
        return self.__identifier == other.identifier

    def __repr__(self):
        """Converts the IdentifyMessage to a string.

        Returns:
            str: String representation of a IdentifyMessage.
        """
        return f"IdentifyMessage(id: {self.__identifier})"

