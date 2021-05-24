"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from processor.scheduling.component.component_interface import IComponent


class ITracker(IComponent):
    """Tracker runner interface that can be run as Scheduler component.
    """

    def track(self, frame_obj, det_obj, tracking_dict):
        """Performs tracking stage using the tracking object.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            det_obj (BoundingBoxes): BoundingBoxes object containing detections from detection stage.
            tracking_dict (dictionary): Dictionary mapping from bounding box ID to object ID

        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        raise NotImplementedError('Tracking stage not implemented')
