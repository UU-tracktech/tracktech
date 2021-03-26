import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import check_img_size, non_max_suppression, apply_classifier, scale_coords, set_logging
from utils.torch_utils import select_device, load_classifier, time_synchronized
from detection.bounding_box import BoundingBox


class Detector:
    """Make it inherit from a generic Detector class"""

    def __init__(self, config):
        self.config = config

        # Initialize
        set_logging()
        self.device = select_device(self.config['device'])
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        if self.device.type == 'cpu':
            print("I am using the CPU. Check CUDA version, or whether Pytorch is installed with CUDA support.")
        else:
            print("I am using GPU")

        # Load model
        self.model = attempt_load(self.config['weights'], map_location=self.device) # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        imgsz = check_img_size(self.config.getint('img-size'), s=self.stride)  # check img_size
        if self.half:
            self.model.half()  # to FP16

        #Set secondary classification, by default off
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, imgsz, imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once


    def detect(self, det_obj):
        """Run detection on a Detection Object

        RETURNS: a Detection Object with filled bounding box list
        """
        # Padded resize
        img = letterbox(det_obj.frame, self.config.getint('img-size'), stride=self.stride)[0]

        # Convert image
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float() # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        #Run inference on the converted image
        t0 = time_synchronized()
        pred = self.model(img, augment=self.config.getboolean('augment'))[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.config.getfloat('conf-thres'), self.config.getfloat('iou-thres'), classes=self.config['classes'],
                                   agnostic=self.config.getboolean('agnostic_nms'))

        # Apply secondary Classifier
        if self.classify:
            pred = apply_classifier(pred, self.modelc, img, det_obj.frame)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], det_obj.frame.shape).round()

                #Get the xyxy, confidence, and class, attach them to det_obj
                for *xyxy, conf, cls in reversed(det):
                    bbox = BoundingBox(i, [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])], self.names[int(cls)], conf)
                    det_obj.bounding_box.append(bbox)

        # Print time (inference + NMS)
        t1 = time_synchronized()
        print(f'Finished processing of frame {det_obj.frame_nr} in ({t1 - t0:.3f}s)')