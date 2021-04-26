"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

from processor.pipeline.tracking.sort.sort import Sort
from processor.pipeline.detection.bounding_box import BoundingBox
from processor.pipeline.tracking.itracker import ITracker


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

    def track(self, track_obj):
        """Performing tracking using SORT tracking to get a tracking ID for all tracked detections.

        Converts detections to correct format, gets trackers from SORT tracking and converts trackers to bounding boxes.
        Tracker doesn't contain classifications, thus the classifications get forgotten.

        Args:
            track_obj (TrackingObj): tracking object used to store bounding boxes for each frame and persistent info.
        """
        detections = track_obj.get_detections()
        trackers = self.sort.update(detections)

        for tracker in trackers:
            bounding_box = BoundingBox(
                identifier=tracker[4],
                rectangle=[
                    int(tracker[0]) / track_obj.width,
                    int(tracker[1]) / track_obj.height,
                    int(tracker[2]) / track_obj.width,
                    int(tracker[3]) / track_obj.height
                ],
                classification='',
                certainty=1
            )

            track_obj.bounding_boxes.append(bounding_box)
