"""Contains re-identification interface, containing the functionality required for an implementation.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import copy

from scipy.spatial.distance import euclidean, cosine

from processor.scheduling.component.i_component import IComponent
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes


class IReIdentifier(IComponent):
    """Superclass for identifiers."""

    def execute_component(self):
        """Function given to scheduler, so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        raise NotImplementedError("execute_component not implemented")

    @property
    def feature_map_size(self):
        """Feature map size getter.

        Returns:
            int: Size of the feature map.
        """
        raise NotImplementedError("Feature map size getter not implemented")

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
        raise NotImplementedError("Re-identify function not implemented")

    def similarity(self, query_features, gallery_features):
        """Calculates the similarity rate between two feature vectors.

        Note:
            Uses euclidean distance or cosine similarity to determine the similarity.

        Args:
            query_features ([float]): the feature vector of the query image.
            gallery_features ([float]): the feature vector of the gallery image.

        Returns:
            float: The similarity value of two feature vectors.
        """
        raise NotImplementedError("Similarity function not implemented")
