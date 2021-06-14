"""Fastreid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import argparse
import copy
import gdown
from scipy.spatial.distance import cosine

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.reidentification.fastreid.fastreid.config import get_cfg
from processor.pipeline.reidentification.fastreid.demo.predictor import FeatureExtractionDemo
from processor.pipeline.reidentification.i_re_identifier import IReIdentifier
import processor.utils.features as UtilsFeatures


class FastReIdentifier(IReIdentifier):
    """Re-id class that uses fast-reid to extract and compare features.

    Attributes:
        extractor (FeatureExtractionDemo): Extractor for the feature vectors.
        config (configparser.SectionProxy): Re-ID configuration.
        threshold (float): Threshold from which a re-identification is included.
    """

    def __init__(self, config):
        """Initialize fast re-identifier.

        Args:
            config (configparser.SectionProxy): Re-ID configuration.
        """

        args = argparse.ArgumentParser(description="Feature extraction with reid models")
        args.config_file = config['config_file_path']
        args.parallel = config.getboolean('parallel')

        # Load config from file and command-line arguments.
        cfg = get_cfg()
        cfg.merge_from_file(args.config_file)
        cfg.freeze()

        # Download the weights if it's not in the directory.
        if not os.path.exists(config['weights_dir_path']):
            os.mkdir(config['weights_dir_path'])

        if not os.path.exists(cfg.MODEL.WEIGHTS):
            url = 'https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/market_sbs_R101-ibn.pth'
            output = cfg.MODEL.WEIGHTS
            gdown.download(url, output, quiet=False)

        self.extractor = FeatureExtractionDemo(cfg, parallel=args.parallel)

        self.config = config
        self.threshold = float(self.config["threshold"])

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
        resized_cutout = UtilsFeatures.resize_cutout(cutout, self.config)

        # Extract the feature from the cutout and convert it to a normal float array.
        feature = self.extractor.run_on_image(resized_cutout).cpu().numpy().tolist()

        return feature

    def extract_features_boxes(self, frame_obj, boxes):
        """Extract features from all bounding boxes generated in the tracking stage.

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

    def similarity(self, query_features, gallery_features):
        """Calculates the similarity rate between two feature vectors.

        Note:
            Uses cosine similarity to determine the similarity rate.
            An alternative would be euclidean distance.

        Args:
            query_features ([float]): the feature vector of the query image.
            gallery_features ([float]): the feature vector of the gallery image.

        Returns:
            float: The similarity value of two feature vectors.
        """
        cosine_similarity = 1 - cosine(query_features, gallery_features)
        return cosine_similarity

    def re_identify(self, frame_obj, track_obj, re_id_data):
        """Performing re-identification using Torchreid.

        This re-identification implementations couple bounding boxes to a tracked subject,
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
                    if similarity_value > self.threshold:
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
