"""Contains StopMessage class which holds information about which object should no longer be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.websocket.i_message import IMessage


class StopMessage(IMessage):
    """StopMessage class that stores data regarding which object to stop tracking."""
    def __init__(self, object_id):
        """Constructor for the StopMessage class.

        Args:
            object_id (int): Identifier of the object that should not be tracked any longer.
        """
        if not isinstance(object_id, int):
            raise TypeError("Object id should be an integer")

        self.__object_id = object_id

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a StopCommand.

        Args:
            message (dict): Python dict representation of an incoming JSON message.

        Returns:
            (StopMessage): StopCommand constructed from the dict.
        """
        if "objectId" not in message.keys():
            raise KeyError("objectId missing")

        object_id = message["objectId"]
        return StopMessage(object_id)

    def to_message(self):
        """Converts the StopMessage to a dict representation.

        Returns:
            (dict): Python dict representation of the message.
        """
        return {
            "type": "stop",
            "objectId": self.__object_id
        }

    @property
    def object_id(self):
        """Get object id.

        Returns:
            (int): Identifier of the object to stop following.
        """
        return self.__object_id

    def __eq__(self, other):
        """Function that checks whether the current StopCommand is the same as the given one.

        Args:
            other (StopMessage): StopCommand to compare with.

        Returns:
            bool: Whether the messages are the same.
        """
        return self.__object_id == other.object_id

    def __repr__(self):
        """Converts the StopMessage to a string.

        Returns:
            str: String representation of a StopMessage.
        """
        return f"StopMessage(object id: {self.__object_id})"
