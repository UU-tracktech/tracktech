import json
import cv2
import math


class DetectionObj:
    """Object that holds all the bounding boxes for a specific frame
    """
    def __init__(self, timestamp, frame, frame_nr):
        self.timestamp = timestamp
        self.frame = frame
        self.frame_nr = frame_nr
        self.bounding_boxes = []

    def draw_rectangles(self) -> None:
        """Draws the bounding boxes on the frame
        """
        red = (0, 0, 255)
        for bounding_box in self.bounding_boxes:
            height, width, _ = self.frame.shape
            self.frame = cv2.rectangle(self.frame,
                                       (int(bounding_box.rectangle[0] * width),
                                       int(bounding_box.rectangle[1] * height)),
                                       (int(bounding_box.rectangle[2] * width),
                                        int(bounding_box.rectangle[3] * height)),
                                       red,
                                       2)
            cv2.rectangle(self.frame,
                          (int(bounding_box.rectangle[0] * width),
                          int(bounding_box.rectangle[1] * height) - 35),
                          (int(bounding_box.rectangle[0] * width + (len(bounding_box.classification) + 4) * 15),
                          int(bounding_box.rectangle[1] * height)),
                          red,
                          -1)
            cv2.putText(self.frame, f'{bounding_box.classification} {round(float(bounding_box.certainty), 2)}',
                        (int(bounding_box.rectangle[0] * width), int(bounding_box.rectangle[1] * height) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

    def to_json(self) -> json:
        """Converts the object to JSON format

        Returns:
            JSON representation of the object

        """
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.timestamp,
            "boxes": [bounding_box.to_json() for bounding_box in self.bounding_boxes],
        })
