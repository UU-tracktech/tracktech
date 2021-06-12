"""Contains StopCommand class which holds information about which object should no longer be tracked.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class StopCommand:
    """StopCommand class that stores data regarding which object to stop tracking."""
    def __init__(self, object_id):
        """Constructor for the StopCommand class.

        Args:
            object_id (int): Identifier of the object that should not be tracked any longer.
        """
        if not isinstance(object_id, int):
            raise TypeError("Object id should be an integer")

        self.__object_id = object_id

    @staticmethod
    def from_json(message):
        if "objectId" not in message.keys():
            raise KeyError("objectId missing")

        object_id = message["objectId"]
        return StopCommand(object_id)

    @property
    def object_id(self):
        return self.__object_id

    def __eq__(self, other):
        return self.__object_id == other.object_id

    def __repr(self):
        return f"StopCommand(object id: {self.__object_id})"

