"""Contains the bounding box class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class BoundingBox:
    """Contains information about a single bounding box.
    """
    def __init__(self, identifier, rectangle, classification, certainty):
        """Inits the bounding box.

        Args:
            identifier (int): identifier of bounding box.
            rectangle (Rectangle): coords of bounding box, contains bottom left and top right coords.
            classification (str): classification of the bounding box.
            certainty (float): certainty/confidence of the bounding box detection.
        """
        self.__identifier = identifier
        self.__rectangle = rectangle
        self.__classification = classification
        self.__certainty = certainty

    def get_identifier(self):
        """Gets bounding box identifier.

        Returns:
            int: identifier of bounding box.
        """
        return self.__identifier

    def get_rectangle(self):
        """Gets Rectangle.

        Returns:
            Rectangle: rectangle composed of bottom right and top left coords.
        """
        return self.__rectangle

    def get_classification(self):
        """Get classification/tag of bounding box.

        Returns:
            str: bounding box classification.
        """
        return self.__classification

    def get_certainty(self):
        """Gets certainty/confidence that bounding box is correctly classified.

        Returns:
            float: certainty/confidence of bounding box detection.
        """
        return self.__certainty
