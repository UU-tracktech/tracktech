"""Has utility files for creating runners for detection and tracking.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.detection.yolor_runner import YolorDetector
from processor.pipeline.tracking.sort_tracker import SortTracker

DETECTOR_SWITCH = {
    'yolov5': (Yolov5Detector, 'Yolov5'),
    'yolor': (YolorDetector, 'Yolor')
}
TRACKER_SWITCH = {
    'sort': (SortTracker, 'SORT')
}


def create_detector(detector_name, configs):
    """Creates and returns a detector of the given type.

    Args:
        detector_name (str): the name of the detector we want.
        configs (ConfigParser): The configurations of the detector.

    Returns:
        IDetector, SectionProxy: Requested detector of the given type combined with its config.
    """
    idetector = DETECTOR_SWITCH[detector_name][0]
    config_section = DETECTOR_SWITCH[detector_name][1]

    config_filter = configs['Filter']
    detector_config = configs[config_section]
    detector = idetector(detector_config, config_filter)
    return detector, detector_config


def create_tracker(tracker_name, configs):
    """Creates and returns a tracker of the given type.

    Args:
        tracker_name (str): The name of the tracker we want.
        configs (ConfigParser): The configurations of the detector.

    Returns:
        ITracker: The requested tracker.
    """
    itracker = TRACKER_SWITCH[tracker_name][0]
    config_section = TRACKER_SWITCH[tracker_name][1]
    tracker_config = configs[config_section]
    tracker = itracker(tracker_config)
    return tracker
