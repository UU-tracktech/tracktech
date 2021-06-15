"""Contains IdentifyCommand class which sends an identifier for the processor to the orchestrator.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.utils.text import bounding_box_to_dict
import json


class IdentifyCommand:
    """Send-only command that holds an identifier for the processor."""
    def __init__(self, identifier):
        """Constructor for the BoxesCommand class.
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier should be a string")

        self.__identifier = identifier

    def to_json(self):
        return json.dumps({
            "type": "identifier",
            "id": self.__identifier
        })

    @property
    def identifier(self):
        return self.__identifier

    def __eq__(self, other):
        return self.__identifier == other.identifier

    def __repr__(self):
        return f"IdentifyCommand(id: {self.__identifier})"

