"""Tracking object component and dict to manage objects.

This file contains a class for tracking objects. Creating an object will automatically add it to a dictionary, which
it removes itself from upon removal.
"""
import json


class TrackingObject:
    """Abstract representation of objects that are tracked in the processors.

    Attributes:
        identifier: An int that serves as the unique identifier to this object.
        feature_map: A json which contains the features of this object, should be sent to all processors.
    """

    def __init__(self):
        """Appends self to objects dictionary upon creation."""

        self.identifier = max(objects.keys(), default=0) + 1
        self.feature_map = {}
        objects[self.identifier] = self

    def update_feature_map(self, feature_map: json):
        """Update feature map of this object.

        Args:
            feature_map:
                json containing the features that should become the new feature map on this object.
        """
        self.feature_map = feature_map
        print(f"updated feature map of object {self.identifier}")

    def remove_self(self):
        """Removes self from objects dict."""
        del objects[self.identifier]


objects = dict()
"""Dictionary which matches an object identifier to 

type: Dict[str, TrackingObject]
"""
