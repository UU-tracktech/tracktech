"""Contains the information object containing all bounding boxes outputted by a stage.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class BoundingBoxes:
    """Object that holds all the bounding boxes for a specific frame."""

    def __init__(self, bounding_boxes):
        """Init information object used as wrapper for bounding boxes list.

        Args:
            bounding_boxes ([BoundingBox]): list of bounding boxes.
        """
        self.__bounding_boxes = bounding_boxes

    def get_bounding_boxes(self):
        """Get bounding boxes.

        Returns:
            [BoundingBox]: list of bounding boxes.
        """
        return self.__bounding_boxes
