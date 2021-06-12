"""Detection abstract class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class IDetector(IComponent):
    """Detection runner interface that can be run as Scheduler component."""

    def execute_component(self):
        """Function given to scheduler so the scheduler can run the detection stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.detect

    def detect(self, frame_obj):
        """Given a frame object, run detection algorithm to find all bounding boxes of objects within the frame.

        Args:
            frame_obj (FrameObj): object containing frame and timestamp.

        Returns:
            BoundingBoxes: returns BoundingBoxes object containing a list of BoundingBox objects.

        Raises:
            NotImplementedError: The function is not overridden in the subclass.
        """
        raise NotImplementedError("Detect function not implemented")
