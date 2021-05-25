"""Torch reid class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import requests

import processor.utils.features as UtilsFeatures
import processor.pipeline.reidentification.ireidentifier
from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor
from scipy.spatial.distance import cosine


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
            req = requests.get('https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download')
            with open(weights_path, 'wb') as file:
                file.write(req.content)

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
        feature = self.extractor(resized_cutout).cpu().numpy().tolist()

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

    def reidentify(self, tracked_boxes, track_features, query_box_id, query_features, threshold):
        """ Performing re-identification using torchreid to possibly couple a detection to an earlier detection of a
        tracked subject.

        Updates list of bounding box by possibly assigning an object ID to an existing bounding box.
        """

        # query_features: features van persoon om te tracken
        # det_features: lijst van features van alle bounding boxes op deze frame
        # threshold: threshold waarbij je bepaalt om ze hetzelfde te noemen

        # TODO: ALs tracking_dict bestaat, update deze dan ook
        raise NotImplementedError()
