"""Contains reidentification interface, containing the functionality required for an implementation.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.scheduling.component.i_component import IComponent


class IReIdentifier(IComponent):
    """Superclass for identifiers."""

    def execute_component(self):
        """Function given to scheduler so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.re_identify

    def extract_features(self, frame_obj, bbox):
        """Extracts features from a single bounding box.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            bbox (BoundingBox): BoundingBox object that stores the bounding box from which we want to extract features.

        Returns:
            [float]: Feature vector of a single bounding box.
        """
        raise NotImplementedError("Extract features function not implemented")

    def extract_features_from_cutout(self, cutout):
        """Given a cutout, extracts the features from it.

        Args:
            cutout (np.ndarray): cutout of the object to extract features from.

        Returns:
            [float]: Feature vector of a single bounding box.
        """
        raise NotImplementedError("Extract features from cutout function not implemented")

    def re_identify(self, frame_obj, track_obj, re_id_data):
        """Performing re-identification using a re-identification implementation.

        Args:
            frame_obj (FrameObj):  frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): List of bounding boxes from tracking stage.
                list has to be of the same length as the list of bounding boxes in the track_obj, and ordered in the
                same way (feature vector i belongs to box i).
            re_id_data (ReidData): Data class containing data about tracked subjects.

        Returns:
            BoundingBoxes: object containing all re-id tracked boxes (bounding boxes where re-id is performed).
        """
        raise NotImplementedError("Reidentification function not implemented")
