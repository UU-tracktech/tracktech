"""Contains the main methods for running YOLOR object detection on a frame

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import sys
import logging
import torch

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.detection.idetector import IDetector
from processor.pipeline.detection.yolor.utils.datasets import letterbox
from processor.pipeline.detection.yolor.utils.general import apply_classifier
from processor.pipeline.detection.yolor.utils.torch_utils import select_device, load_classifier, time_synchronized
from processor.pipeline.detection.yolor.models.models import Darknet


class YolorDetector(IDetector):
    """Implementation of YOLOR repository

    """
    def __init__(self, config, filters):
        """Initiate the YOLOR detector

        Args:
            config (ConfigParser): YOLOR config file.
            filters (): Filtering for boundingBoxes.
        """
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(curr_dir, './yolor'))

        self.config = config
        self.filter = []
        with open(filters['targets_path']) as filter_names:
            self.filter = filter_names.read().splitlines()
        print('I am filtering on the following objects: ' + str(self.filter))

        # Initialize
        logging.basicConfig(
            format="%(message)s",
            level=logging.INFO)
        if self.config['device'] != 'cpu':
            if not torch.cuda.is_available():
                logging.info("CUDA unavailable")
                self.config['device'] = 'cpu'
        self.device = select_device(self.config['device'])
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        if self.device.type == 'cpu':
            logging.info("I am using the CPU. Check CUDA version,"
                         "or whether Pytorch is installed with CUDA support.")
        else:
            logging.info("I am using GPU")

        # Load model
        if self.device.type == 'cpu':
            self.model = Darknet(self.config['cfg_path'], self.config['img-size'])
        else:
            self.model = Darknet(self.config['cfg_path'], self.config['img-size']).cuda()
        self.model.load_state_dict(torch.load(self.config['weights_path'], map_location=self.device)['model'])
        self.model.to(self.device).eval()
        if self.half:
            self.model.half()  # to FP16

        # Second-stage classifier
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            # load weights
            self.modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model'])
            self.modelc.to(self.device).eval()

        # Get names
        self.names = self.load_classes(config['names_path'])

        img = torch.zeros((1, 3, self.config.getint('img-size'), self.config.getint('img-size')), device=self.device)
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once

    # pylint: disable=duplicate-code
    def detect(self, frame_obj):
        """Run detection on a Detection Object.

        Args:
            frame_obj (FrameObj): information object containing frame and timestamp.

        Returns:
            BoundingBoxes: a BoundingBoxes object containing a list of Boundingbox objects
        """
        bounding_boxes = []

        # Resize
        img = letterbox(frame_obj.get_frame(), self.config.getint('img-size'), auto_size=self.config.getint('stride'))[0]
        img = self.convert_image(img, self.device, self.half)

        # Inference
        start_time = time_synchronized()
        pred = self.generate_predictions(img, self.model, self.config)

        print('converted image')
        # Apply secondary Classifier
        if self.classify:
            pred = apply_classifier(pred, self.modelc, img, frame_obj.get_frame())

        # Create bounding boxes based on the predictions
        self.create_bounding_boxes(pred, img, frame_obj, bounding_boxes, self.filter, self.names)
        boxes = BoundingBoxes(bounding_boxes)

        # Print time (inference + NMS)
        print(f'Finished processing of frame {frame_obj.get_timestamp()} in ({time_synchronized() - start_time:.3f}s)')

        return boxes

    @staticmethod
    def load_classes(path):
        """Loads the classes to detect

        Args:
            path (str): path to the file the classes need to get loaded of

        Returns:
            [str]: List of empty strings
        """
        # Loads *.names file at 'path'
        with open(path, 'r') as file:
            names = file.read().split('\n')
        # filter removes empty strings (such as last line)
        return list(filter(None, names))
