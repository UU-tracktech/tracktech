"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import json
import cv2
import numpy as np

from processor.pipeline.detection.detection_obj import DetectionObj


class TrackingObj:
    """Tracking object containing all information of the tracking stage result of an iteration.
    """
    def __init__(self):
        """Inits TrackingObj with default values.
        """
        self.det_obj: DetectionObj = None
        self.frame = None
        self.height = 1
        self.width = 1
        self.bounding_boxes = []

    def update(self, det_obj: DetectionObj):
        """Update TrackingObj with det_obj and set bounding_boxes to an empty list.

        Args:
            det_obj (DetectionObj): DetectionObj containing all detections from the detection stage.
        """
        self.det_obj = det_obj

        self.frame = det_obj.frame
        self.height, self.width, _ = det_obj.frame.shape

        self.bounding_boxes = []

    def get_detections(self):
        """Converts bounding boxes of detections to detections (numpy.ndarray) in SORT tracking format.

        Returns:
            numpy.ndarray: NumPy array containing detections in format expected by SORT tracking.
        """
        if len(self.det_obj.bounding_boxes) == 0:
            return np.empty((0, 5))

        sort_detections = []
        for bounding_box in self.det_obj.bounding_boxes:
            sort_detections.append([
                bounding_box.rectangle[0] * self.width,
                bounding_box.rectangle[1] * self.height,
                bounding_box.rectangle[2] * self.width,
                bounding_box.rectangle[3] * self.height,
                bounding_box.certainty
            ])

        return np.asarray(sort_detections)

    def draw_rectangles(self):
        """Draws the bounding boxes on the frame with ID.
        """
        blue = (255, 0, 0)

        for bounding_box in self.bounding_boxes:
            # Object bounding box.
            cv2.rectangle(self.frame,
                          (int(bounding_box.rectangle[0] * self.width),
                           int(bounding_box.rectangle[1] * self.height)),
                          (int(bounding_box.rectangle[2] * self.width),
                           int(bounding_box.rectangle[3] * self.height)),
                          blue,
                          2
                          )

            # Tag background.
            cv2.rectangle(self.frame,
                          (int(bounding_box.rectangle[0] * self.width),
                           int(bounding_box.rectangle[1] * self.height) - 35),
                          (int(bounding_box.rectangle[0] * self.width + (len(f'{bounding_box.identifier}') * 12)),
                           int(bounding_box.rectangle[1] * self.height)),
                          blue,
                          -1
                          )

            # Tag bounding box ID.
            cv2.putText(self.frame,
                        f'{int(bounding_box.identifier)}',
                        (int(bounding_box.rectangle[0] * self.width),
                         int(bounding_box.rectangle[1] * self.height) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 0, 0),
                        2
                        )

        return self.frame

    def to_json(self):
        """Converts the object to JSON format.

        Returns:
            JSON representation of the object.
        """
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.det_obj.timestamp,
            "boxes": [bounding_box.to_dict() for bounding_box in self.bounding_boxes],
        })

    def to_dict(self):
        """Converts the object to a dict containing frame, timestamp, and list of bounding boxes

        Returns:
            A python dict of the object

        """
        return {
            "frame": self.frame,
            "frameId": self.det_obj.timestamp,
            "boxes": [bounding_box.to_dict() for bounding_box in self.bounding_boxes]
        }
