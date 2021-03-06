"""Mock detector for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import random

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.detection.i_detector import IDetector
from processor.data_object.rectangle import Rectangle


class FakeDetector(IDetector):
    """A fake detector, which does nonsense detections."""
    def detect(self, _):
        """Appends a couple random bounding boxes.

        Returns:
            BoundingBoxes: Dummy bounding boxes.
        """
        bounding_boxes = []

        # Append random boxes for detection.
        for i in range(random.randrange(5)):
            bounding_boxes.append(BoundingBox(i, Rectangle(0, 0, 1, 1), 'fake class', 0.5))

        return BoundingBoxes(bounding_boxes)
