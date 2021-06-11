"""Contains sort_oh tracker.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import numpy as np
from typing import List

from processor.pipeline.tracking.sort_oh.libs.tracker import Sort_OH
from processor.data_object.bounding_box import BoundingBox
from processor.pipeline.tracking.itracker import ITracker
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle


class SortOHTracker(ITracker):
    """Tracker of SORT tracking.
    Contains the Sort tracking class and gets trackers from this class with each track() call.
    Attributes:
        config (configparser.SectionProxy): SORT tracker configuration.
        sort (Sort): Sort tracking class.
    """
    def __init__(self, config):
        """Inits SortTracker with SORT tracker configuration.
        Args:
            config (configparser.SectionProxy): SORT tracker configuration.
        """
        self.config = config
        self.sort = Sort_OH(max_age=config.getint('max_age'),
                            min_hits=config.getint('min_hits'),
                            iou_threshold=config.getfloat('iou_threshold'))

    def execute_component(self):
        """Function given to scheduler so the scheduler can run the tracking stage.
        Returns:
            function: function that the scheduler can run.
        """
        return self.track

    def track(self, frame_obj, det_obj, re_id_data):
        """Performing tracking using SORT tracking to get a tracking ID for all tracked detections.
        Converts detections to correct format, gets trackers from SORT tracking and converts trackers to bounding boxes.
        Tracker doesn't contain classifications, thus the classifications get forgotten.
        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            det_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of detection stage
            re_id_data (ReidData): Object containing data necessary for re-identification
        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        width, height = frame_obj.shape

        # Get bounding boxes into format expected by SORT tracker.
        det_bounding_boxes = det_obj.bounding_boxes
        sort_detections = []
        for bounding_box in det_bounding_boxes:
            sort_detections.append((np.asarray([
                bounding_box.rectangle.x1 * width,
                bounding_box.rectangle.y1 * height,
                bounding_box.rectangle.x2 * width,
                bounding_box.rectangle.y2 * height,
                bounding_box.certainty]),
                bounding_box.classification,
                bounding_box.certainty))

        # Get all tracked objects found in current frame.
        trackers = self.sort.update(sort_detections, (width, height))

        # Turn tracked objects into BoundingBox objects.
        bounding_boxes = []

        for tracker in trackers:
            bounding_box = BoundingBox(
                identifier=int(tracker[0][4]),
                rectangle=Rectangle(
                    max(int(tracker[0][0]) / width, 0),
                    max(int(tracker[0][1]) / height, 0),
                    min(int(tracker[0][2]) / width, 1),
                    min(int(tracker[0][3]) / height, 1),
                ),
                classification=tracker[1],
                certainty=tracker[2],
                object_id=re_id_data.get_object_id_for_box(int(tracker[0][4]))
            )
            bounding_boxes.append(bounding_box)

        return BoundingBoxes(bounding_boxes)
