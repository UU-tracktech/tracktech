class BoundingBox:
    def __init__(self, identifier, rectangle, classification, certainty):
        self.identifier = identifier
        self.rectangle = rectangle  #[x1, y1, x2, y2] where (x1, y1) and (x2, y2) are two diagonal opposing corners of the box
        self.feature = None
        self.classification = classification
        self.certainty = certainty
