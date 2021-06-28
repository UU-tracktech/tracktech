"""Datawriter super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""


class IDataWriter:
    """Superclass for objects that write data"""
    def __init__(self):
        """Method for initializing the data writer"""

    def write(self, bounding_boxes, shape):
        """Method that is called to write some bounding boxes to the file.

        Args:
             bounding_boxes (BoundingBoxes): An object containing the bounding boxes that are detected in a frame.
             shape (int, int): A tuple containing the width and height of the frames.
        """
        raise NotImplementedError('There is no implementation for a default write method.')

    def close(self):
        """Method for closing the data writer object"""
        raise NotImplementedError('There is no implementation for a default close method.')
