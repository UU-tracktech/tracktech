"""Fastreid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import argparse
import logging
import gdown
import torch

from processor.pipeline.reidentification.fastreid.fastreid.config import get_cfg
from processor.pipeline.reidentification.fastreid.demo.predictor import FeatureExtractionDemo
from processor.pipeline.reidentification.pytorch_re_identifier import PytorchReIdentifier
from processor.utils.features import resize_cutout


class FastReIdentifier(PytorchReIdentifier):
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

        args = argparse.ArgumentParser(description='Feature extraction with reid models')
        args.config_file = config['config_file_path']
        args.parallel = config.getboolean('parallel')

        # Load config from file and command-line arguments.
        cfg = get_cfg()
        cfg.merge_from_file(args.config_file)
        weight_name = cfg.MODEL.WEIGHTS
        weight_path = os.path.join(config['weights_dir_path'], weight_name)
        cfg.MODEL.WEIGHTS = weight_path

        if not torch.cuda.is_available():
            logging.info('Fast-Reid is using CPU')
            cfg.MODEL.DEVICE = 'cpu'
        else:
            logging.info('Fast-Reid is using GPU')

        cfg.freeze()

        # Download the weights if it's not in the directory.
        if not os.path.exists(config['weights_dir_path']):
            os.mkdir(config['weights_dir_path'])

        if not os.path.exists(weight_path):
            url = 'https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/market_sbs_R101-ibn.pth'
            gdown.download(url, weight_path, quiet=False)

        extractor = FeatureExtractionDemo(cfg, parallel=args.parallel)
        super().__init__(config, extractor)

    def extract_features(self, cutouts):
        """Given cutouts, extracts the features from it.

        Args:
            cutouts (np.ndarray): cutout of the object to extract features from.

        Returns:
            [float]: Feature vector of a single bounding box.
        """
        features = []
        for cutout in cutouts:
            features.append(self.extractor.run_on_image(cutout).cpu().numpy().tolist())

        return features

    def extract_features_from_image(self, image):
        """Extract features from an image.

        Args:
            image (np.ndarray): the image of the object to extract features from.

        Returns:
            [float]: Feature vector of an image.
        """
        resized_image = resize_cutout(image, self.config)

        return self.extractor.run_on_image(resized_image).cpu().numpy().tolist()[0]
