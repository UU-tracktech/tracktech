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
            image_id (int): id of the image.
        """
        self.__bounding_boxes = bounding_boxes
        self.__image_id = image_id

    def get_bounding_boxes(self):
        """Get bounding boxes.

        Returns:
            [BoundingBox]: list of bounding boxes.
        """
        return self.__bounding_boxes

    def get_image_id(self):
        """Gets image id.

        Returns:
            __image_io (int): Id of image.
        """
        return self.__image_id
