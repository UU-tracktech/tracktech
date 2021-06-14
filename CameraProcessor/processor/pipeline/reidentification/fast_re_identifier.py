"""Fast reid class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import argparse
import gdown

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
        feature = self.extractor.run_on_image(resized_cutout).cpu().numpy().tolist()

        return feature
