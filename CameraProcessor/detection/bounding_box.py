import json

class BoundingBox:
    def __init__(self, identifier, rectangle, classification, certainty):
        self.identifier = identifier
        self.rectangle = rectangle
        self.feature = None
        self.classification = classification
        self.certainty = certainty

    def to_json(self):
        str = json.dumps({
            "boxId": self.identifier,
            "rect": self.rectangle,
        })

        # We need to decode the string so we don't get top-level double encoding
        return json.JSONDecoder().decode(str)