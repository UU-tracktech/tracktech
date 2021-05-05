"""Contains the main methods for running YOLOv5 object detection on a frame

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import sys
import logging
from numpy import random
import numpy as np
import torch
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.pipeline.detection.yolov5.models.experimental import attempt_load
from processor.pipeline.detection.yolov5.utils.datasets import letterbox
from processor.pipeline.detection.yolov5.utils.general import check_img_size,\
    non_max_suppression, apply_classifier,\
    scale_coords, set_logging
from processor.pipeline.detection.yolov5.utils.torch_utils import select_device,\
    load_classifier, time_synchronized
from processor.pipeline.detection.idetector import IDetector
from processor.data_object.rectangle import Rectangle


class Yolov5Detector(IDetector):
    """Make it inherit from a generic Detector class.

    """

    def __init__(self, config, filters):
        """Initialize Yolov5Detector.

        Args:
            config (ConfigParser): Yolov5 config file.
            filters (): Filtering for boundingBoxes.
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

    def detect(self, frame_obj):
        """Run detection on a Detection Object.

        Args:
            frame_obj (FrameObj): information object containing frame and timestamp.

        Returns:
            DetectionObj: a Detection Object with filled bounding box list.
        """
        # Padded resize
        bounding_boxes = []
        img = letterbox(frame_obj.get_frame(), self.config.getint('img-size'), stride=self.stride)[0]

        # Convert image
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Run inference on the converted image
        time_zero = time_synchronized()
        pred = self.model(img, augment=self.config.getboolean('augment'))[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.config.getfloat('conf-thres'),
                                   self.config.getfloat('iou-thres'),
                                   classes=self.config['classes'],
                                   agnostic=self.config.getboolean('agnostic_nms'))

        # Apply secondary Classifier
        if self.classify:
            pred = apply_classifier(pred, self.modelc, img, frame_obj.get_frame())

        # Process detections
        for _, det in enumerate(pred):  # detections per image
            if len(det) > 0:
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame_obj.get_frame().shape).round()

                bb_id = 0
                # Get the xyxy, confidence, and class, attach them to det_obj
                for *xyxy, conf, cls in reversed(det):
                    width, height = frame_obj.get_shape()
                    bbox = BoundingBox(
                        bb_id,
                        Rectangle(int(xyxy[0])/width, int(xyxy[1])/height, int(xyxy[2])/width, int(xyxy[3])/height),
                        self.names[int(cls)],
                        conf
                    )
                    if any(x == bbox.get_classification() for x in self.filter):
                        bounding_boxes.append(bbox)
                        bb_id += 1

        # Print time (inference + NMS)
        time_one = time_synchronized()
        print(f'Finished processing of frame {frame_obj.get_timestamp()} in ({time_one - time_zero:.3f}s)')

        return BoundingBoxes(bounding_boxes)
