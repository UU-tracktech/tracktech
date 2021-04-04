import json
import cv2


class DetectionObj:
    """
    Contains all the bounding boxes for a specific frame
    """
    def __init__(self, timestamp, frame, frame_nr):
        self.timestamp = timestamp
        self.frame = frame
        self.frame_nr = frame_nr
        self.bounding_boxes = []

    def draw_rectangles(self):
        """
        Draws the bounding boxes on the frame
        """
        red = (255, 0, 0)
        for bounding_box in self.bounding_boxes:
            self.frame = cv2.rectangle(self.frame,
                                       tuple(bounding_box.rectangle[:2]),
                                       tuple(bounding_box.rectangle[2:]),
                                       red,
                                       2)

    def to_json(self):
        """
        Converts the object to JSON format
        Returns: JSON representation of the object

        """
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.timestamp,
            "boxes": [bounding_box.to_json() for bounding_box in self.bounding_boxes],
        })
