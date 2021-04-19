import json
from typing import List



class BoundingBox:
    """Contains information about a single bounding box
    """
    def __init__(self, identifier: int, rectangle: List[int], classification: str, certainty: float):
        """

        Args:
            identifier (int):
            rectangle :
            classification:
            certainty:
        """
        self.identifier = identifier
        self.rectangle = rectangle
        if len(rectangle) != 4:
            raise AttributeError('Invalid length for bounding box in BoundingBox.rectangle')
        self.feature = None
        self.classification = classification
        self.certainty = certainty

    def to_json(self) -> json:
        """Converts the object to JSON format
        Returns: JSON representation of the object

        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        """Readies the data of the bounding box object
        for conversion into a JSON object

        Returns: A python dict for the corresponding JSON object

        """
        return {
            "boxId": self.identifier,
            "rect": self.rectangle
        }
