import cv2
import json
from .bounding_box import BoundingBox

class DetectionObj:
    def __init__(self, timestamp, frame, frame_nr):
        self.timestamp = timestamp
        self.frame = frame
        self.frame_nr = frame_nr
        self.bounding_box = []

    def draw_rectangles(self):
        red = (255, 0, 0)
        for bounding_box in self.bounding_box:
            self.frame = cv2.rectangle(self.frame,
                                       tuple(bounding_box.rectangle[:2]),
                                       tuple(bounding_box.rectangle[2:]),
                                       red,
                                       2)

    def mock_bounding_boxes(self):
        boxes = []
        for i in range(1, 10):
            boxes.append(BoundingBox(i, (0, 0, 10 * i, 10 * i), None, 0))
        return boxes


    def to_json(self):
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.frame_nr,
            "boxes": [bounding_box.to_json() for bounding_box in self.bounding_box],
        })