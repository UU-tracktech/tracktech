"""Contains UpdateMessage class which holds an updated feature_map for a followed object.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.websocket.i_message import IMessage


class UpdateMessage(IMessage):
    """Contains UpdateMessage class which holds an updated feature_map for a followed object."""
    def __init__(self, object_id, feature_map):
        """Constructor for the UpdateMessage class.

        Args:
            object_id (int): Identifier of the object that should be followed.
            feature_map ([float]): Feature map of the object that should be followed.
        """
        if not isinstance(object_id, int):
            raise TypeError('Object id should be an integer')

        self.__object_id = object_id
        self.__feature_map = feature_map

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a UpdateMessage.

        Args:
            message (dict): Python dict representation of an incoming JSON message.

        Returns:
            (BoxesMessage): UpdateMessage constructed from the dict.
        """
        if 'featureMap' not in message.keys():
            raise KeyError('featureMap missing')

        if 'objectId' not in message.keys():
            raise KeyError('objectId missing')

        object_id = message['objectId']
        feature_map = message['featureMap']

        return UpdateMessage(object_id, feature_map)

    def to_message(self):
        """Converts the UpdateMessage to a dict representation.

        Returns:
            (dict): Python dict representation of the message.
        """
        return {
            'type': 'featureMap',
            'objectId': self.__object_id,
            'featureMap': self.__feature_map
        }

    @property
    def object_id(self):
        """Get object identifier.

        Returns:
            (int): Id of the object.
        """
        return self.__object_id

    @property
    def feature_map(self):
        """Get feature map.

        Returns:
            ([float]): Feature map of the object.
        """
        return self.__feature_map

    def __eq__(self, other):
        """Function that checks whether the current UpdateCommand is the same as the given one.

        Args:
            other (UpdateMessage): UpdateCommand to compare with.

        Returns:
            bool: Whether the messages are the same.
        """
        return (self.__object_id == other.object_id
                and self.__feature_map == other.feature_map)

    def __repr__(self):
        """Converts the UpdateMessage to a string.

        Returns:
            str: String representation of a UpdateMessage.
        """
        return f'UpdateMessage(object id: {self.__object_id}'\
               f' feature map: {self.__feature_map})'
