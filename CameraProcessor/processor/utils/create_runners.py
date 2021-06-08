"""Has utility files for creating runners for detection and tracking.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.detection.yolor_runner import YolorDetector
from processor.pipeline.tracking.sort_tracker import SortTracker
from processor.pipeline.reidentification.torchreid_runner import TorchReIdentifier
from processor.pipeline.reidentification.fastreid_runner import FastReIdentifier

DETECTOR_SWITCH = {
    'yolov5': (Yolov5Detector, 'Yolov5'),
    'yolor': (YolorDetector, 'Yolor')
}
TRACKER_SWITCH = {
    'sort': (SortTracker, 'SORT')
}
REID_SWITCH = {
    'torchreid': (TorchReIdentifier, 'TorchReid'),
    'fastreid': (FastReIdentifier, 'FastReid')
}


def create_detector(detector_name, configs):
    """Creates and returns a detector of the given type.

    Args:
        detector_name (str): the name of the detector we want.
        configs (dict): The configurations of the detector.

    Returns:
        IDetector: Requested detector of the given type
    """
    idetector = DETECTOR_SWITCH[detector_name][0]
    config_section = DETECTOR_SWITCH[detector_name][1]

    config_filter = configs['Filter']
    detector_config = configs[config_section]
    detector = idetector(detector_config, config_filter)
    return detector


def create_tracker(tracker_name, configs):
    """Creates and returns a tracker of the given type.

    Args:
        tracker_name (str): The name of the tracker we want.
        configs (dict): The configurations of the tracker.

    Returns:
        ITracker: The requested tracker.
    """
    itracker = TRACKER_SWITCH[tracker_name][0]
    config_section = TRACKER_SWITCH[tracker_name][1]
    tracker_config = configs[config_section]
    tracker = itracker(tracker_config)
    return tracker

def create_reidentifier(reid_name, configs):
    """Creates and returns a re-identifier of the given type.

    Args:
        reid_name (str): the name of the re-identifier we want.
        configs (dict): The configurations of the re-identifier.

    Returns:
        IReIdentifier: Requested re-identifier of the given type
    """
    ireidentifier = REID_SWITCH[reid_name][0]
    config_section = REID_SWITCH[reid_name][1]
    reid_config = configs[config_section]
    reidentifier = ireidentifier(reid_config)
    return reidentifier
