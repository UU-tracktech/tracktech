"""Contains BoxesCommand class which holds information about bounding boxes in the current frame.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.utils.text import bounding_box_to_dict
import json


class BoxesCommand:
    """Send-only command that contains the bounding boxes in the current frame."""
    def __init__(self, frame_id, bounding_boxes):
        """Constructor for the BoxesCommand class.
        """
        if not isinstance(frame_id, float):
            raise TypeError("Frame id should be an float")

        if not isinstance(bounding_boxes, BoundingBoxes):
            raise TypeError("Bounding boxes should be of type BoundingBoxes")

        self.__frame_id = frame_id
        self.__bounding_boxes = bounding_boxes

    def to_json(self):
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.__frame_id,
            "boxes": [bounding_box_to_dict(bounding_box) for bounding_box in self.__bounding_boxes],
        })

    @property
    def frame_id(self):
        return self.__frame_id

    @property
    def bounding_boxes(self):
        return self.__bounding_boxes

    def __eq__(self, other):
        return self.__frame_id == other.frame_id and self.__bounding_boxes == other.bounding_boxes

    def __repr__(self):
        return f"BoxesCommand(frame id: {self.__frame_id} boxes: {self.__bounding_boxes})"

