"""Contains main video processing pipeline function

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class ITracker:
    """Tracker interface.
    """
    def track(self, frame_obj, det_obj):
        """Performs tracking stage using the tracking object.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            det_obj (BoundingBoxes): BoundingBoxes object containing detections from detection stage.

        Returns:
            BoundingBoxes: object containing all trackers (bounding boxes of tracked objects).
        """
        raise NotImplementedError('Tracking stage not implemented')
