import os
import json
import logging
import random

from processor.pipeline.detection.bounding_box import BoundingBox
from processor.pipeline.detection.idetector import IDetector


class FakeDetector(IDetector):
    """A fake detector which does nonsense detections

    """

    def detect(self, det_obj):
        """Appends a couple random bounding boxes

        """
        det_obj.bounding_boxes = []
        for i in range(random.randrange(5)):
            bbox = BoundingBox(i, [0, 0, 1, 1], "fake class", 0.5)
            det_obj.bounding_boxes.append(bbox)
        logging.info(f"Finished processing frame {det_obj.frame_nr}")
