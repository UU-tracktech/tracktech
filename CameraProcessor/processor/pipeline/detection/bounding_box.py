import json
from typing import List


class BoundingBox:
    """Contains information about a single bounding box.
    """
    def __init__(self, identifier: int, rectangle: List[int], classification: str, certainty: float):
        """Inits the bounding box.

        Args:
            identifier (int): identifier of bounding box.
            rectangle (List[int]): [x_left, y_bot, x_right, y_top], coords of bounding box.
            classification (str): classification of the bounding box.
            certainty (float): certainty/confidence of the bounding box detection.
        """
        self.identifier = identifier
        self.rectangle = rectangle
        if len(rectangle) != 4:
            raise AttributeError('Invalid length for bounding box in BoundingBox.rectangle')
        self.feature = None
        self.classification = classification
        self.certainty = certainty

    def to_json(self) -> json:
        """Converts the object to JSON format.

        Returns:
            json: JSON representation of the object.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        """Readies the data of the bounding box object for conversion into a JSON object.

        Returns:
            dict: Python dict for the corresponding JSON object

        """
        return {
            "boxId": self.identifier,
            "rect": self.rectangle
        }
