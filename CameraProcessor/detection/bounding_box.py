class BoundingBox:
    def __init__(self, identifier, rectangle, classification, certainty):
        self.identifier = identifier
        self.rectangle = rectangle
        self.feature = None
        self.classification = classification
        self.certainty = certainty
