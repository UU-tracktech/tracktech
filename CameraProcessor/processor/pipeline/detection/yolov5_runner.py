"""Contains the main methods for running YOLOv5 object detection on a frame

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import sys
import logging
from numpy import random
import torch

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.detection.yolov5.models.experimental import attempt_load
from processor.pipeline.detection.yolov5.utils.datasets import letterbox
from processor.pipeline.detection.yolov5.utils.general import check_img_size,\
    apply_classifier,set_logging
from processor.pipeline.detection.yolov5.utils.torch_utils import select_device,\
    load_classifier, time_synchronized
from processor.pipeline.detection.idetector import IDetector


class Yolov5Detector(IDetector):
    """Make it inherit from a generic Detector class.

    """

    def __init__(self, config, filters):
        """Initialize Yolov5Detector.

        Args:
            config (ConfigParser): Yolov5 config file.
            filters (ConfigParser): Filter for boundingBoxes.
        """
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(curr_dir, './yolov5'))

        self.config = config
        self.filter = []
        with open(filters['targets_path']) as filter_names:
            self.filter = filter_names.read().splitlines()
        print('I am filtering on the following objects: ' + str(self.filter))

        # Initialize
        set_logging()
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

        # load FP32 model
        self.model = attempt_load(self.config['weights_path'],
                                  map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        imgsz = check_img_size(self.config.getint('img-size'), s=self.stride)  # check img_size
        if self.half:
            self.model.half()  # to FP16

        # Set secondary classification, by default off
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(
                torch.load('weights/resnet101.pt',
                           map_location=self.device)['model']
            ).to(self.device).eval()

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

        if self.device.type != 'cpu':
            self.model(
                torch.zeros(1, 3, imgsz,
                            imgsz).to(self.device).type_as(next(self.model.parameters())))
            # run once

    # pylint: disable=duplicate-code
    def detect(self, frame_obj):
        """Run detection on a Detection Object.

        Args:
            frame_obj (FrameObj): information object containing frame and timestamp.

        Returns:
            BoundingBoxes: a BoundingBoxes object containing a list of Boundingbox objects
        """
        # Padded resize
        bounding_boxes = []

        img = letterbox(frame_obj.get_frame(), self.config.getint('img-size'), stride=self.stride)[0]
        img = self.convert_image(img, self.device, self.half)

        # Run inference on the converted image
        start_time = time_synchronized()
        pred = self.generate_predictions(img, self.model, self.config)

        # Apply secondary Classifier
        if self.classify:
            pred = apply_classifier(pred, self.modelc, img, frame_obj.get_frame())

        # Create bounding boxes based on the predictions
        self.create_bounding_boxes(pred, img, frame_obj, bounding_boxes, self.filter, self.names)

        # Print time (inference + NMS)
        print(f'Finished processing of frame {frame_obj.get_timestamp()} in ({time_synchronized() - start_time:.3f}s)')

        return BoundingBoxes(bounding_boxes)
