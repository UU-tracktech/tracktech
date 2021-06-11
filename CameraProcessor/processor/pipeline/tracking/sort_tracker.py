"""Contains sort tracker.

This tracker predicts the position of a detection.
Based on detection boxes it predicts the position of the tracker on the next few frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.pipeline.tracking.sort.sort import Sort
from processor.pipeline.tracking.i_sort_tracker import ISortTracker


class SortTracker(ISortTracker):
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

    def track(self, frame_obj, detection_boxes, re_id_data):
        """Performing tracking using SORT tracking to get a tracking ID for all tracked detections.

        Converts detections to correct format, gets trackers from SORT tracking and converts trackers to bounding boxes.
        Tracker doesn't contain classifications, thus the classifications get forgotten.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            detection_boxes (BoundingBoxes): BoundingBoxes object that has the bounding boxes of detection stage
            re_id_data (ReidData): Object containing data necessary for re-identification

        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        # Get bounding boxes into format expected by SORT tracker.
        detections = self.convert_boxes_to_sort(detection_boxes, frame_obj.shape)

        # Get all tracked objects found in current frame.
        sort_detections = self.sort.update(detections)

        return self.parse_boxes_from_sort(sort_detections, frame_obj.shape, re_id_data)
