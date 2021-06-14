"""Torch reid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import gdown

import processor.utils.features as UtilsFeatures
from processor.pipeline.reidentification.i_re_identifier import IReIdentifier
from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor


class TorchReIdentifier(IReIdentifier):
    """Re-id class that uses torch-reid to extract and compare features.

    Attributes:
        extractor (FeatureExtractor): Extractor for the feature vectors.
        config (configparser.SectionProxy): Re-ID configuration.
        threshold (float): Threshold from which a re-identification is included.
    """

    def __init__(self, config):
        """Initialize torch re-identifier.

        Args:
            config (configparser.SectionProxy): Re-ID configuration.
        """

        # The path where the model weight file should be located.
        weights_path = os.path.join(config['weights_dir_path'], config['model_name'] + '.pth')

        # Download the weights if it's not in the directory.
        if not os.path.exists(config['weights_dir_path']):
            os.mkdir(config['weights_dir_path'])

        if not os.path.exists(weights_path):
            url = 'https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download'
            output = weights_path
            gdown.download(url, output, quiet=False)

        # Initialize the feature extractor of torch re-id.
        self.extractor = FeatureExtractor(
            model_name=config['model_name'],
            model_path=weights_path,
            device=config['device'])

        super().__init__(config)
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
        feature = self.extractor(resized_cutout).cpu().numpy().tolist()[0]

        return feature

    def extract_features_from_cutout(self, cutout):
        """Extracts features from a cutout.

        Args:
            cutout (np.ndarray): the cutout containing the object we want to extract features from

        Returns:
            [float]: Feature vector of the cutout
        """
        # Resize the cutout.
        resized_cutout = UtilsFeatures.resize_cutout(cutout, self.config)

        return self.extractor(resized_cutout).cpu().numpy().tolist()[0]
