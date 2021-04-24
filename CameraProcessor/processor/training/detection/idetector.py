"""Detection abstract class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
from processor.pipeline.detection.detection_obj import DetectionObj


class IDetector:
    """Superclass for detectors

    """

    def detect(self, det_obj: DetectionObj):
        """Function that runs detection on a Detection Object

        Args:
            det_obj: Detection object that gets modified during this function run
        """
        raise NotImplementedError("Detect function not implemented")
