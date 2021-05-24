import os
import requests

from processor.pipeline.reidentification.torchreid.torchreid.utils import FeatureExtractor
from scipy.spatial.distance import cosine
from processor.utils.features import slice_bounding_box, resize_cutout


from processor.pipeline.reidentification.ireidentifier import IReIdentifier


class TorchReIdentifier(IReIdentifier):

    def __init__(self, model_name, device, configs):
        """ Initialize torch re-identifier

        Args:
            model_name (string): The name of the model weights
            device (string): determines whether or not to use the gpu or cpu
            configs (configparser.SectionProxy): Re-ID configuration
        """

        # the path where the model weight file should be located
        weights_path = 'pipeline/reidentification/torchreid/weights/' + model_name + '.pth'

        # download the weights if it's not in the directory
        if not os.path.exists('pipeline/reidentification/torchreid/weights'):
            os.mkdir('pipeline/reidentification/torchreid/weights')

        if not os.path.exists(weights_path):
            r = requests.get('https://drive.google.com/u/0/uc?id=1vduhq5DpN2q1g4fYEZfPI17MJeh9qyrA&export=download')
            with open(weights_path, 'wb') as f:
                f.write(r.content)

        # Initialize the feature extractor of torch re-id
        self.extractor = FeatureExtractor(
            model_name=model_name,
            model_path=weights_path,
            device=device)

        self.configs = configs

    def extract_features(self, frame_obj, track_obj):
        """ Extracts features from all bounding boxes generated in the tracking stage by generating a
        cutout of the bounding boxes and feeding them to the feature extractor of Torchreid.

        Args:
            frame_obj (FrameObj): frame object storing OpenCV frame and timestamp.
            track_obj (BoundingBoxes): BoundingBoxes object that has the bounding boxes of the tracking stage

        Returns:
            float[]: returns the feature vectors of the tracked objects.
        """

        features = []

        for tracked_box in track_obj.get_bounding_boxes():
            # Cutout the bounding box from the frame and resize the cutout to the right size
            cutout = slice_bounding_box(tracked_box, frame_obj.get_frame())
            resized_cutout = resize_cutout(cutout, self.configs)
            # Extract the feature from the cutout
            feature = self.extractor(resized_cutout)
            features.append(feature.cpu().numpy())

        return features

    def similarity(self, query_features, gallery_features):
        """

        Args:
            query_features: the feature vector of the query image
            gallery_features: the feature vector of the gallery image

        Returns: float: returns the cosine similarity of two feature vectors

        """
        cosine_similarity = 1 - cosine(query_features, gallery_features)
        return cosine_similarity

    def reidentify(self, tracked_boxes, track_features, query_boxID, query_features, threshold):
        """ Performing re-identification using torchreid to possibly couple a detection to an earlier detection of a
        tracked subject.

        Updates list of bounding box by possibly assigning an object ID to an existing bounding box.
        """

        # query_features: features van persoon om te tracken
        # det_features: lijst van features van alle bounding boxes op deze frame
        # threshold: threshold waarbij je bepaalt om ze hetzelfde te noemen

        # TODO: ALs tracking_dict bestaat, update deze dan ook
        raise NotImplementedError()
