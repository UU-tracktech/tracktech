"""Contains BoxesMessage class which holds information about bounding boxes in the current frame.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.utils.text import bounding_boxes_to_dict
from processor.websocket.i_message import IMessage


class BoxesMessage(IMessage):
    """Message that contains the bounding boxes in the current frame."""
    def __init__(self, frame_id, bounding_boxes):
        """Constructor for the BoxesMessage class.

        Args:
            frame_id (float): identifier of the frame.
            bounding_boxes (BoundingBoxes): bounding boxes in the frame.

        Raises:
            TypeError: One or more of the attributes given has the wrong type
        """
        if not isinstance(frame_id, float):
            raise TypeError('Frame id should be a float.')
        if not isinstance(bounding_boxes, BoundingBoxes):
            raise TypeError('bounding_boxes must be of type BoundingBoxes')

        self.__frame_id = frame_id
        self.__bounding_boxes = bounding_boxes

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a BoxesCommand.

        Args:
            message (dict): Python dict representation of an incoming JSON message.

        Returns:
            (BoxesMessage): BoxesCommand constructed from the dict.

        Raises:
            KeyError: One or more of the expected keys needed for the boxes message is missing.
        """
        if 'frameId' not in message.keys():
            raise KeyError('frameId missing')

        if 'boxes' not in message.keys():
            raise KeyError('objectId missing')

        frame_id = message['frameId']
        boxes = message['boxes']

        return BoxesMessage(frame_id, BoundingBoxes(boxes, frame_id))

    def to_message(self):
        """Converts the BoxesMessage to a dict representation.

        Returns:
            (dict): Python dict representation of the message.
        """
        return bounding_boxes_to_dict(self.__bounding_boxes, self.__frame_id)

    @property
    def frame_id(self):
        """Get frame id.

        Returns:
            (float): Id of the frame.
        """
        return self.__frame_id

    @property
    def bounding_boxes(self):
        """Get bounding boxes.

        Returns:
            (BoundingBoxes): List of bounding boxes.
        """
        return self.__bounding_boxes

    def __eq__(self, other):
        """Function that checks whether the current BoxesCommand is the same as the given one.

        Args:
            other (BoxesMessage): BoxesCommand to compare with.

        Returns:
            bool: Whether the messages are the same.
        """
        return self.__frame_id == other.frame_id and self.__bounding_boxes == other.bounding_boxes

    def __repr__(self):
        """Converts the BoxesMessage to a string.

        Returns:
            str: String representation of a BoxesMessage.
        """
        return f'BoxesMessage(frame id: {self.__frame_id} boxes: {self.__bounding_boxes})'
