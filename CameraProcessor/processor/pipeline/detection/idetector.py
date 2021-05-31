"""Detection abstract class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import numpy as np
import torch

from processor.scheduling.component.component_interface import IComponent
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.pipeline.detection.yolor.utils.general import non_max_suppression, scale_coords


class IDetector(IComponent):
    """Detection runner interface that can be run as Scheduler component.
    """

    def detect(self, frame_obj):
        """Given a frame object, run detection algorithm to find all bounding boxes of objects within frame.

        Args:
            frame_obj (FrameObj): object containing frame and timestamp.

        Returns:
            BoundingBoxes: returns BoundingBoxes object containing a list of BoundingBox objects
        """
        raise NotImplementedError("Detect function not implemented")

    @staticmethod
    def convert_image(img, device, half):
        """Converts the image to the size used for the detection.

        Args:
            img (Tensor): Image in a tensor representation
            device (device): What device to convert image on
            half (bool): Whether to half the image

        Returns:
            Tensor: Image that is converted
        """
        # Convert image.
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        return img

    @staticmethod
    def generate_predictions(img, model, configs):
        """Generates the predictions of the detection.

        Args:
            img (Tensor): 2
            model (model): Model that gets used
            configs (SectionProxy): Yolo section of the configuration

        Returns:
            Tensor: Tensor containing the predictions the detection made
        """
        pred = model(img, augment=configs.getboolean('augment'))[0]

        # Apply NMS.
        return non_max_suppression(pred, configs.getfloat('conf-thres'),
                                   configs.getfloat('iou-thres'),
                                   classes=configs['classes'],
                                   agnostic=configs.getboolean('agnostic_nms'))

    @staticmethod
    def create_bounding_boxes(pred, img, frame_obj, bounding_boxes, filter_types, names):
        """Creates the bounding boxes of the detection.

        Args:
            pred ([Tensor]): List of tensors containing the predictions
            img (Tensor): Image stored in a tensor
            frame_obj (FrameObj): Object containing the frame
            bounding_boxes ([BoundingBoxes]): Bounding boxes in which to store the predictions
            filter_types ([str]): What detection types to filter on
            names ([str]): The complete list of types that get detected
        """
        # Detections per image.
        for _, det in enumerate(pred):
            if det is not None and len(det) > 0:
                # Rescale boxes from img_size to im0 size.
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame_obj.get_frame().shape).round()

                bb_id = 0
                # Get the xyxy, confidence, and class, attach them to det_obj.
                for *xyxy, conf, cls in reversed(det):
                    width, height = frame_obj.get_shape()
                    bbox = BoundingBox(
                        bb_id,
                        Rectangle(int(xyxy[0]) / width, int(xyxy[1]) / height, int(xyxy[2]) / width,
                                  int(xyxy[3]) / height),
                        names[int(cls)],
                        conf.item()
                    )
                    if any(x == bbox.get_classification() for x in filter_types):
                        bounding_boxes.append(bbox)
                        bb_id += 1
