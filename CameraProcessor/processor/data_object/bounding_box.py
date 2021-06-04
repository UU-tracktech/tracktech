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

    def set_object_id(self, new_id):
        """Set the object id of a bounding box. Used when a box has been re-identified to contain a tracked object.

        Args:
            new_id (int): The updated object_id of the box.

        Raises:
            ValueError: if the box already was assigned to an object.
        """
        if self.__object_id is not None:
            raise ValueError("Box already has an object ID")

        self.__object_id = new_id
