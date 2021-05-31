"""Mock tracker for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import logging
import random

from processor.data_object.rectangle import Rectangle
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.tracking.itracker import ITracker


class FakeTracker(ITracker):
    """A fake detector which does nonsense detections.

    Attributes:
        config (ConfigParser): Configurations of the tracker.
        sort ()
    """
    def __init__(self, config=None):
        """Inits the fake tracker.

        Args:
            config (ConfigParser): Configurations of the tracker.
        """
        self.config = config
        self.sort = None

    # pylint: disable=unused-argument
    def track(self, _, bounding_boxes, reid_data):
        """Appends a couple random bounding boxes.

        Args:
            bounding_boxes (BoundingBoxes): Detection boxes given to the tracker.
            reid_data (ReidData): Object containing all the reid data .
        """
        tracked_bounding_boxes = []

        # Append some tracked boxes.
        for i in range(random.randrange(5)):
            bbox = BoundingBox(i, Rectangle(0, 0, 1, 1), "fake class", 0.5)
            tracked_bounding_boxes.append(bbox)

        logging.info("Finished processing frame %placeholder%")
        return BoundingBoxes(tracked_bounding_boxes)
