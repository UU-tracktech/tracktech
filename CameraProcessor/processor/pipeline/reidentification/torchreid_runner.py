"""Torch reid class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import gdown

import processor.utils.features as UtilsFeatures
import processor.pipeline.reidentification.ireidentifier
from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor
from scipy.spatial.distance import cosine
from processor.data_object.reid_data import ReidData


class TorchReIdentifier(processor.pipeline.reidentification.ireidentifier.IReIdentifier):
    """Re-id class that uses torch-reid to extract and compare features.
    """

    def __init__(self, model_name, device, configs):
        """Initialize torch re-identifier.

        Args:
            model_name (string): The file name of the model weights.
            device (string): determines whether or not to use the gpu or cpu.
            configs (configparser.SectionProxy): Re-ID configuration.
        """

        # the path where the model weight file should be located
        weights_path = os.path.join(configs['weights_dir_path'], model_name + '.pth')

        # download the weights if it's not in the directory
        if not os.path.exists(configs['weights_dir_path']):
            os.mkdir(configs['weights_dir_path'])

        if not os.path.exists(weights_path):
            url = 'https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download'
            output = weights_path
            gdown.download(url, output, quiet=False)

        # Initialize the feature extractor of torch re-id
        self.extractor = FeatureExtractor(
            model_name=model_name,
            model_path=weights_path,
            device=device)

        self.configs = configs

    def extract_features(self, frame_obj, bbox):
        """Extracts features from a single bounding box by generating a
        cutout of the bounding boxes and feeding them to the feature extractor of Torchreid.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            bbox (BoundingBox): BoundingBox object that stores the bounding box from which we want to extract features.

        Returns:
             [float]: Feature vector of single bounding box.

        """
        # Cutout the bounding box from the frame and resize the cutout to the right size
        cutout = UtilsFeatures.slice_bounding_box(bbox, frame_obj.get_frame())
        resized_cutout = UtilsFeatures.resize_cutout(cutout, self.configs)

        # Extract the feature from the cutout and convert it to a normal float array
        feature = self.extractor(resized_cutout).cpu().numpy().tolist()[0]

        return feature

    def extract_features_boxes(self, frame_obj, track_obj):
        """Extracts features from all bounding boxes generated in the tracking stage.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage.

        Returns:
            [[float]]: returns the feature vectors of the tracked objects.
        """

        features = []

        for tracked_box in track_obj.get_bounding_boxes():
            features.append(self.extract_features(frame_obj, tracked_box))

        return features

    def similarity(self, query_features, gallery_features):
        """Calculates the similarity rate between two feature vectors.

        Args:
            query_features ([float]): the feature vector of the query image.
            gallery_features ([float]): the feature vector of the gallery image.

        Returns: float: returns the cosine similarity of two feature vectors.

        """
        cosine_similarity = 1 - cosine(query_features, gallery_features)
        return cosine_similarity

    def re_identify(self, track_obj, box_features, re_id_data, threshold):
        """ Performing re-identification using torchreid to possibly couple bounding boxes to a tracked subject
        which is not currently detected on the camera. Updates list of bounding box by possibly assigning an object ID
        to an existing bounding box. Does not return anything, just updates the existing list.

        Args:
            track_obj (BoundingBoxes): List of bounding boxes from tracking stage
            box_features ([[float]]): List of feature vectors for bounding boxes from tracking stage. Note that this
            list has to be of the same length as the list of bounding boxes in track_obj, and ordered in the same
            way (feature vector i belongs to box i).
            re_id_data (ReidData): Data class containing data about tracked subjects
            threshold (float): Threshold for similarity to match tracked subject to bounding box
        """
        # track_obj: contains tracked bounding boxes
        tracked_bounding_boxes = track_obj.get_bounding_boxes()

        # Loop over all objects being followed
        for query_id in re_id_data.get_queries():
            query_feature = re_id_data.get_feature_for_query(query_id)

            # track_features: list of feature vectors in same order as bounding boxes
            # Loop over the detected features in the frame
            for i in range(len(box_features)):
                # if the bounding box is already assigned to an object, don't compare it
                if tracked_bounding_boxes[i].get_object_id() is None:
                    if self.similarity(query_feature, box_features[i]) > threshold:
                        box_id = tracked_bounding_boxes[i].get_identifier()

                        # Store that this box id belongs to a certain object id
                        re_id_data.add_query_box(box_id, query_id)

                        # Update object id of the box
                        tracked_bounding_boxes[i].set_object_id(query_id)

                        print(f"Re-Id of object {query_id} in box {box_id}")

        # TODO : objects that are still on screen (box id in list is on screen) should not be reidentified
        # TODO : test with custom video
        # TODO : ?
