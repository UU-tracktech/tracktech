"""Contains tracking interface.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class ITracker(IComponent):
    """Tracker runner interface that can be run as Scheduler component."""

    def execute_component(self):
        """Function given to scheduler so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.track

    def track(self, frame_obj, det_obj, re_id_data):
        """Performs tracking stage using the tracking object.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            det_obj (BoundingBoxes): BoundingBoxes object containing detections from detection stage.
            re_id_data (ReidData): Object containing data necessary for re-identification

        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        raise NotImplementedError('Tracking stage not implemented')
