"""Contains reidentification interface, containing the functionality required for an implementation.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.component_interface import IComponent


class IReIdentifier(IComponent):
    """Superclass for identifiers."""

    def execute_component(self):
        """Function given to scheduler so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.re_identify

    def extract_features(self, frame_obj, track_obj):
        """Given a det_obj object, extract the features of it.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage.

        Returns:
            [float]: Feature vectors of the tracked objects.
        """
        raise NotImplementedError("Extract features function not implemented")

    def re_identify(self, frame_obj, track_obj, re_id_data):
        """Performing re-identification using a re-idintification implementation.

        Args:
            frame_obj (FrameObj):  frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): List of bounding boxes from tracking stage.
                list has to be of the same length as the list of bounding boxes in track_obj, and ordered in the same
                way (feature vector i belongs to box i).
            re_id_data (ReidData): Data class containing data about tracked subjects.

        Returns:
            BoundingBoxes: object containing all re-id tracked boxes (bounding boxes where re-id is performed).
        """
        raise NotImplementedError("Reidentification function not implemented")
