"""Contains the information object containing all bounding boxes outputted by a stage.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class BoundingBoxes:
    """Object that holds all the bounding boxes for a specific frame."""

    def __init__(self, bounding_boxes, image_id=''):
        """Inits information object used as wrapper for bounding boxes list.

        Args:
            bounding_boxes ([BoundingBox]): list of bounding boxes.
            image_id (str): id of the image.
        """
        self.__bounding_boxes = bounding_boxes
        self.__image_id = image_id

    @property
    def bounding_boxes(self):
        """Get bounding boxes.

        Returns:
            [BoundingBox]: list of bounding boxes.
        """
        return self.__bounding_boxes

    @property
    def image_id(self):
        """Gets image id.

        Returns:
            __image_io (int): Id of image.
        """
        return self.__image_id

    def __eq__(self, other):
        """Function that checks whether the current bounding box is the same as the given one.

        Args:
            other (BoundingBoxes): BoundingBoxes to compare with.

        Returns:
            bool: Whether all bounding boxes are the same inside the object.
        """
        return self.bounding_boxes == other.bounding_boxes

    def __repr__(self):
        """String representation of the bounding boxes.

        Returns:
            str: Bounding boxes inside the list.
        """
        return f'BoundingBoxes(imageid: {self.image_id} boxes: {self.bounding_boxes})'

    def __iter__(self):
        """Iterates the bounding boxes inside the list.

        Returns:
            list_iterator: Iterator for the list of bounding boxes.
        """
        return self.__bounding_boxes.__iter__()

    def __len__(self):
        """Number of boxes stored inside the object.

        Returns:
            int: Length of the number of boxes.
        """
        return len(self.__bounding_boxes)
