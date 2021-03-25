import json


class TrackingObject:
    identifier: int
    feature_map: json

    # Append self to objects dictionary upon creation
    def __init__(self):
        self.identifier = max(objects.keys(), default=0) + 1
        objects[self.identifier] = self

    # Update feature map of this object
    def update_feature_map(self, feature_map):
        self.feature_map = feature_map
        print(f"updated feature map of object {self.identifier}")

    # Remove self from objects dict
    def remove_self(self):
        del objects[self.identifier]


objects = dict()
