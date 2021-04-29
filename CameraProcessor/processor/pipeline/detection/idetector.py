"""Detection abstract class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


class IDetector:
    """Superclass for detectors
    """

    def detect(self, frame_obj):
        """Given a frame object, run detection algorithm to find all bounding boxes of objects within frame.

        Args:
            frame_obj (FrameObj): object containing frame and timestamp.

        Returns:
            DetectionObj: return bounding boxes in frame wrapped in DetectionObj.
        """
        raise NotImplementedError("Detect function not implemented")
