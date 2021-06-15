"""Contains re-identification superclass for pytorch implementations.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import copy

from scipy.spatial.distance import euclidean, cosine

from processor.pipeline.reidentification.i_re_identifier import IReIdentifier
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes


class PytorchReIdentifier(IReIdentifier):
    """Superclass for identifiers."""

    def __init__(self, config):
        """Init for Pytorch Re-identifier which saves config.

        Args:
            config (configparser.SectionProxy): the re-id configuration to pass
        """
        self.config = config
        self.threshold = float(self.config["threshold"])

    def execute_component(self):
        """Function given to scheduler, so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.re_identify

    @property
    def feature_map_size(self):
        """Feature map size getter.

        Returns:
            int: Size of the feature map.
        """
        raise NotImplementedError("Feature map size getter not implemented")

    def extract_features_boxes(self, frame_obj, boxes):
        """Extracts features from all bounding boxes generated in the tracking stage.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            boxes (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage.

        Returns:
            [[float]]: Feature vectors of the tracked objects.
        """
        features = []

        for box in boxes:
            features.append(self.extract_features(frame_obj, box))

        return features

    def extract_features(self, frame_obj, bbox):
        """Extract features from a single bounding box.

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
        tracked_bounding_boxes = track_obj.bounding_boxes
        box_features = self.extract_features_boxes(frame_obj, track_obj)

        # Copy the original bounding boxes to a new list.
        bounding_boxes = copy.copy(tracked_bounding_boxes)

        # Loop over all objects being followed.
        for query_id in re_id_data.get_queries():
            query_feature = re_id_data.get_feature_for_query(query_id)

            # List 'track_features' contains feature vectors in same order as bounding boxes.
            # Loop over the detected features in the frame.
            for i, feature in enumerate(box_features):
                # If the bounding box is already assigned to an object, don't compare it.
                if tracked_bounding_boxes[i].object_id is None:
                    # Calculate the similarity value of the 2 feature vectors.
                    similarity_value = self.similarity(query_feature, feature)
                    if self.config.get("distance") == "euclidean":
                        similarity_bool = similarity_value < self.threshold
                    elif self.config.get("distance") == "cosine":
                        similarity_bool = similarity_value > self.threshold
                    else:
                        similarity_bool = False
                        raise ValueError(f"Distance metric {self.config.get('distance')} "
                                         f"is not a valid distance metric.")
                    if similarity_bool:
                        box_id = tracked_bounding_boxes[i].identifier

                        # Store that this box id belongs to a certain object id.
                        re_id_data.add_query_box(box_id, query_id)

                        # Update object id of the box.
                        bounding_boxes[i] = BoundingBox(
                            identifier=box_id,
                            rectangle=tracked_bounding_boxes[i].rectangle,
                            classification=tracked_bounding_boxes[i].classification,
                            certainty=tracked_bounding_boxes[i].certainty,
                            object_id=query_id
                        )

                        print(f"Re-Id of object {query_id} in box {box_id}")

        return BoundingBoxes(bounding_boxes)

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
        # pylint: disable=no-else-return.
        if self.config.get("distance") == "euclidean":
            return euclidean(query_features, gallery_features)
        elif self.config.get("distance") == "cosine":
            return 1 - cosine(query_features, gallery_features)
        raise ValueError(f"Distance metric {self.config.get('distance')} is not a valid distance metric.")
        # pylint: enable=no-else-return.
