"""Contains re-identification superclass for pytorch implementations.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from scipy.spatial.distance import euclidean, cosine

from processor.pipeline.reidentification.i_re_identifier import IReIdentifier
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
import processor.utils.features as UtilsFeatures


class PytorchReIdentifier(IReIdentifier):
    """Superclass for identifiers."""

    def __init__(self, config, extractor):
        """Init for Pytorch Re-identifier which saves config.

        Args:
            config (configparser.SectionProxy): the re-id configuration to pass
            extractor (FeatureExtractor): The feature extractor used by the re-identifier
        """
        self.config = config
        self.extractor = extractor
        self.threshold = float(self.config['threshold'])

    def execute_component(self):
        """Function given to scheduler, so the scheduler can run the tracking stage.

        Returns:
            function: function that the scheduler can run.
        """
        return self.re_identify

    def extract_cutouts(self, frame_obj, boxes):
        """Extracts cutouts from all bounding boxes generated in the tracking stage.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            boxes (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage.

        Returns:
            cutouts ([np.ndarray]): A list of resized cutouts of the BoundingBoxes.
        """
        cutouts = []
        for box in boxes:
            cutout = UtilsFeatures.slice_bounding_box(box, frame_obj.frame)
            resized_cutout = UtilsFeatures.resize_cutout(cutout, self.config)
            cutouts.append(resized_cutout)

        return cutouts

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
        cutouts = self.extract_cutouts(frame_obj, tracked_bounding_boxes)
        box_features = self.extract_features(cutouts)

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
                    if self.config.get('distance') == 'euclidean':
                        similarity_bool = similarity_value < self.threshold
                    elif self.config.get('distance') == 'cosine':
                        similarity_bool = similarity_value > self.threshold
                    else:
                        similarity_bool = False
                        raise ValueError(f'Distance metric {self.config.get("distance")} '
                                         f'is not a valid distance metric.')
                    if similarity_bool:
                        box_id = tracked_bounding_boxes[i].identifier

                        # Store that this box id belongs to a certain object id.
                        re_id_data.add_query_box(box_id, query_id)

                        # Update object id of the box.
                        tracked_bounding_boxes[i] = BoundingBox(
                            identifier=box_id,
                            rectangle=tracked_bounding_boxes[i].rectangle,
                            classification=tracked_bounding_boxes[i].classification,
                            certainty=tracked_bounding_boxes[i].certainty,
                            object_id=query_id
                        )

                        print(f'Re-Id of object {query_id} in box {box_id}')

        return track_obj

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
        if self.config.get('distance') == 'euclidean':
            return euclidean(query_features, gallery_features)
        elif self.config.get('distance') == 'cosine':
            return 1 - cosine(query_features, gallery_features)
        raise ValueError(f'Distance metric {self.config.get("distance")} is not a valid distance metric.')
        # pylint: enable=no-else-return.
