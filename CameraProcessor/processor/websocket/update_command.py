"""Contains Update class which holds an updated feature_map for a followed object.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json


class UpdateCommand:
    """StopCommand class that stores data regarding which object to stop tracking."""
    def __init__(self, object_id, feature_map):
        """Constructor for the StopCommand class.

        Args:
            object_id (int): Identifier of the object that should not be tracked any longer.
        """
        if not isinstance(object_id, int):
            raise TypeError("Object id should be an integer")

        # TODO: Type checking of the feature map

        self.__object_id = object_id
        self.__feature_map = feature_map

    def to_json(self):
        return json.dumps({
            "type": "featureMap",
            "objectId": self.__object_id,
            "featureMap": self.__feature_map
        })

    @staticmethod
    def from_message(message):
        if "featureMap" not in message.keys():
            raise KeyError("featureMap missing")

        if "objectId" not in message.keys():
            raise KeyError("objectId missing")

        object_id = message["objectId"]
        feature_map = message["featureMap"]

        return UpdateCommand(object_id, feature_map)

    @property
    def object_id(self):
        return self.__object_id

    @property
    def feature_map(self):
        return self.__feature_map

    def __eq__(self, other):
        return (self.__object_id == other.object_id
                and self.__feature_map == other.feature_map)

    def __repr__(self):
        return f'UpdateCommand(object id: {self.__object_id}'\
               f'feature map: {self.__feature_map})'
