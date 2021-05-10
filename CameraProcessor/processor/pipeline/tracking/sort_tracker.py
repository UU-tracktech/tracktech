"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import numpy as np

from processor.pipeline.tracking.sort.sort import Sort
from processor.data_object.bounding_box import BoundingBox
from processor.pipeline.tracking.itracker import ITracker
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle


class SortTracker(ITracker):
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
        self.sort = Sort(max_age=config.getint('max_age'),
                         min_hits=config.getint('min_hits'),
                         iou_threshold=config.getfloat('iou_threshold')
                         )

    def track(self, frame_obj, det_obj):
        """Performing tracking using SORT tracking to get a tracking ID for all tracked detections.

        Converts detections to correct format, gets trackers from SORT tracking and converts trackers to bounding boxes.
        Tracker doesn't contain classifications, thus the classifications get forgotten.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            det_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of detection stage

        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        width, height = frame_obj.get_shape()

        # Get bounding boxes into format expected by SORT tracker.
        det_bounding_boxes = det_obj.get_bounding_boxes()

        if len(det_bounding_boxes) == 0:
            detections = np.empty((0, 5))
        else:
            sort_detections = []

            for bounding_box in det_bounding_boxes:
                sort_detections.append([
                    bounding_box.get_rectangle().get_x1() * width,
                    bounding_box.get_rectangle().get_y1() * height,
                    bounding_box.get_rectangle().get_x2() * width,
                    bounding_box.get_rectangle().get_y2() * height,
                    bounding_box.get_certainty()
                ])

            detections = np.asarray(sort_detections)

        # Get all tracked objects found in current frame.
        trackers = self.sort.update(detections)

        # Turn tracked objects into BoundingBox objects.
        bounding_boxes = []

        for tracker in trackers:
            bounding_box = BoundingBox(
                identifier=int(tracker[4]),
                rectangle=Rectangle(
                    int(tracker[0]) / width,
                    int(tracker[1]) / height,
                    int(tracker[2]) / width,
                    int(tracker[3]) / height
                ),
                classification='',
                certainty=1
            )

            bounding_boxes.append(bounding_box)

        return BoundingBoxes(bounding_boxes)
