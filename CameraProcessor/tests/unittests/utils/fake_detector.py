"""Mock detector for testing.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import logging
import random

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.detection.idetector import IDetector
from processor.data_object.rectangle import Rectangle


class FakeDetector(IDetector):
    """A fake detector which does nonsense detections

    """

    def detect(self, frame_obj):
        """Appends a couple random bounding boxes

        """
        bounding_boxes = []
        for i in range(random.randrange(5)):
            bounding_boxes.append(BoundingBox(i, Rectangle(0, 0, 1, 1), "fake class", 0.5))

        return BoundingBoxes(bounding_boxes)
