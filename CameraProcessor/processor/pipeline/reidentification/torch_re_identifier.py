"""Torch reid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import gdown

from processor.pipeline.reidentification.pytorch_re_identifier import PytorchReIdentifier
from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor
from processor.utils.features import resize_cutout


class TorchReIdentifier(PytorchReIdentifier):
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
            gdown.download(url, weights_path, quiet=False)

        # Initialize the feature extractor of torch re-id.
        extractor = FeatureExtractor(
            model_name=config['model_name'],
            model_path=weights_path,
            device=config['device'])

        super().__init__(config, extractor)

    def extract_features(self, cutouts):
        """Extract features from a list of cutouts.

        Args:
            cutouts ([np.ndarray]): A list of cutouts of the objects to extract features from.

        Returns:
             [[float]]: Feature vectors of the cutouts.
        """

        return self.extractor(cutouts).cpu().numpy().tolist()

    def extract_features_from_image(self, image):
        """Extract features from an image.

        Args:
            image (np.ndarray): the image of the object to extract features from.

        Returns:
            [float]: Feature vector of an image.
        """
        resized_image = resize_cutout(image, self.config)

        return self.extractor(resized_image).cpu().numpy().tolist()[0]
