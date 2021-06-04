"""Torch reid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import copy
import gdown

from scipy.spatial.distance import euclidean

import processor.utils.features as UtilsFeatures
import processor.pipeline.reidentification.ireidentifier
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor


class TorchReIdentifier(processor.pipeline.reidentification.ireidentifier.IReIdentifier):
    """Re-id class that uses torch-reid to extract and compare features.

    Attributes:
        extractor (FeatureExtractor): Extractor for the feature vectors.
        configs (configparser.SectionProxy): Re-ID configuration.
        threshold (float): Threshold from which a re-identification is included.
    """

    def __init__(self, model_name, configs):
        """Initialize torch re-identifier.

        Args:
            model_name (string): The file name of the model weights.
            configs (configparser.SectionProxy): Re-ID configuration.
        """

        # The path where the model weight file should be located.
        weights_path = os.path.join(configs['weights_dir_path'], model_name + '.pth')

        # Download the weights if it's not in the directory.
        if not os.path.exists(configs['weights_dir_path']):
            os.mkdir(configs['weights_dir_path'])

        if not os.path.exists(weights_path):
            url = 'https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download'
            output = weights_path
            gdown.download(url, output, quiet=False)

        # Initialize the feature extractor of torch re-id.
        self.extractor = FeatureExtractor(
            model_name=model_name,
            model_path=weights_path,
            device=configs['device'])

        self.configs = configs
        self.threshold = float(self.configs["threshold"])

    def extract_features(self, frame_obj, bbox):
        """Extracts features from a single bounding box.

        This is achieved by generating a cutout of the bounding boxes
        and feeding them to the feature extractor of Torchreid.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            bbox (BoundingBox): BoundingBox object that stores the bounding box from which we want to extract features.

        Returns:
             [float]: Feature vector of single bounding box.
        """
        # Cutout the bounding box from the frame and resize the cutout to the right size.
        cutout = UtilsFeatures.slice_bounding_box(bbox, frame_obj.frame)
        resized_cutout = UtilsFeatures.resize_cutout(cutout, self.configs)

        # Extract the feature from the cutout and convert it to a normal float array.
        feature = self.extractor(resized_cutout).cpu().numpy().tolist()[0]

        return feature

    def extract_features_boxes(self, frame_obj, tracked_boxes):
        """Extracts features from all bounding boxes generated in the tracking stage.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            tracked_boxes (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage.

        Returns:
            [[float]]: Feature vectors of the tracked objects.
        """
        features = []

        for tracked_box in tracked_boxes:
            features.append(self.extract_features(frame_obj, tracked_box))

        return features

    def similarity(self, query_features, gallery_features):
        """Calculates the similarity rate between two feature vectors.

        Note:
            Uses euclidean distance to determine the similarity.
            An alternative would be cosine similarity.

        Args:
            query_features ([float]): the feature vector of the query image.
            gallery_features ([float]): the feature vector of the gallery image.

        Returns:
            float: The similarity value of two feature vectors.
        """
        euclidean_distance = euclidean(query_features, gallery_features)
        return euclidean_distance

    def re_identify(self, frame_obj, track_obj, re_id_data):
        """Performing re-identification using torchreid.

        This re-identification implementations couple bounding boxes to a tracked subject
        which is not currently detected on the camera. Updates list of bounding box by possibly assigning an object ID
        to an existing bounding box.

        Args:
            frame_obj (FrameObj): Frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): List of bounding boxes from tracking stage.
                list has to be of the same length as the list of bounding boxes in track_obj, and ordered in the same
                way (feature vector i belongs to box i).
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
                    if similarity_value < self.threshold:
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
