"""Mock tracker for testing.

"""
import logging
import random

from processor.pipeline.detection.bounding_box import BoundingBox
from processor.pipeline.tracking.itracker import ITracker


class FakeTracker(ITracker):
    """A fake detector which does nonsense detections

    """
    def __init__(self, config=None):
        self.config = config
        self.sort = None

    def track(self, track_obj):
        """Appends a couple random bounding boxes
        """
        track_obj.bounding_boxes = []
        for i in range(random.randrange(5)):
            bbox = BoundingBox(i, [0, 0, 1, 1], "fake class", 0.5)
            track_obj.bounding_boxes.append(bbox)
        logging.info("Finished processing frame %placeholder%")
