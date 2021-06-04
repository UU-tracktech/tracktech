"""Contains the bounding box class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class BoundingBox:
    """Contains information about a single bounding box."""

    def __init__(self, identifier, rectangle, classification, certainty, object_id=None):
        """Init the bounding box.

        Args:
            identifier (int): identifier of bounding box.
            rectangle (Rectangle): coords of bounding box, contains bottom left and top right coords.
            classification (str): classification of the bounding box.
            certainty (float): certainty/confidence of the bounding box detection.
            object_id (int): id assigned to object depicted by the bounding box
        """
        self.__identifier = identifier
        self.__rectangle = rectangle
        self.__classification = classification
        self.__certainty = certainty
        self.__object_id = object_id

    @property
    def identifier(self):
        """Bounding box identifier getter.

        Returns:
            int: identifier of bounding box.
        """
        return self.__identifier

    @property
    def rectangle(self):
        """Get Rectangle.

        Returns:
            Rectangle: rectangle composed of bottom right and top left coords.
        """
        return self.__rectangle

    @property
    def classification(self):
        """Get classification/tag of bounding box.

        Returns:
            str: bounding box classification.
        """
        return self.__classification

    @property
    def certainty(self):
        """Get certainty/confidence that bounding box is correctly classified.

        Returns:
            float: certainty/confidence of bounding box detection.
        """
        return self.__certainty

    @property
    def object_id(self):
        """Gets object id of tracked object depicted by the bounding box (can be None).

        Returns:
            int: certainty/confidence of bounding box detection.
        """
        return self.__object_id

    def __eq__(self, other):
        """Function that checks whether the current bounding box is the same as the given one.

        Args:
            other (BoundingBox): BoundingBox to compare with.

        Returns:
            bool: Whether the bounding boxes are the same.
        """
        return self.__identifier == other.identifier and \
            self.__rectangle == other.rectangle and \
            self.__classification == other.classification and \
            self.__certainty == other.certainty and \
            self.__object_id == other.object_id

    def __repr__(self):
        """Converts the bounding box object to a string.

        Returns:
            str: String representation of an bounding box.
        """
        return f'BoundingBox(type: "{self.__classification}" certainty: {self.__certainty} ' \
               f'identifier: {self.__identifier} id: {self.__object_id} ' \
               f'rectangle: {self.__rectangle})'
