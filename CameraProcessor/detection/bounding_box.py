class BoundingBox:
    def __init__(self, identifier, rectangle, classification, certainty):
        self.identifier = identifier
        self.rectangle = rectangle
        if len(rectangle) != 4:
            raise AttributeError('Invalid length for bounding box in BoundingBox.rectangle')
        self.feature = None
        self.classification = classification
        self.certainty = certainty
