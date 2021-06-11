"""Tracking object component and dict to manage objects.

This file contains a class for tracking objects. Creating an object will automatically add it to a dictionary, which
it removes itself from upon removal.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from datetime import datetime

from src.objects.object_management import objects, objectHistory
import src.utility.logger as logger


class TrackingObject:
    """Abstract representation of objects that are tracked in the processors.

    Attributes:
        identifier (int): Serves as the unique identifier to this object.
        image (string): Serialised string containing the cutout image of this object.
        feature_map (json): Contains the features of this object, should be sent to all processors.
    """

    def __init__(self, image):
        """Appends self to objects dictionary upon creation.

        Args:
            image (string):
                Serialised string containing the cutout image of this object.
        """

        # Identifier can be guaranteed to be unique if the maximum of the history is used plus 1.
        self.identifier = max(objectHistory, default=0) + 1
        self.image = image
        # Feature map is expected to be sent by the processor later on.
        self.feature_map = {}
        objects[self.identifier] = (self, datetime.now())
        objectHistory.append(self.identifier)

    def update_feature_map(self, feature_map):
        """Updates feature map of this object.

        Args:
            feature_map (json):
                json containing the features that should become the new feature map on this object.
        """
        self.feature_map = feature_map
        logger.log(f"updated feature map of object {self.identifier}")

    def remove_self(self):
        """Removes self from objects dict."""
        del objects[self.identifier]

    def log_spotting(self, processor_id):
        """Writes a spotting of this object to a log file.

        Args:
            processor_id (int): Identifier of the processor
        """
        file = open(f"tracking_timelines/tracking_logs_{self.identifier}.txt", "a")
        file.write(json.dumps({
            "timeStamp": datetime.now().strftime("%Y/%m/%d | %H:%M:%S"),
            "processorId": processor_id
        }))
        file.write(",\n")
        file.close()
