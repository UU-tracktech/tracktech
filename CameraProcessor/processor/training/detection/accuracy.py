"""
File containing the accuracy class
"""
# Determine training set
# Determine test set
# Verification sets

# Run test set in epochs

import configparser
# Determine accuracy of a bounding box estimate
import os
from typing import List

from podm.podm import BoundingBox, get_pascal_voc_metrics
from podm.visualize import plot_precision_recall_curve

from processor.input.image_capture import ImageCapture
from processor.training.pre_annotations import PreAnnotations


class AccuracyObject:
    """
    This class is used to test the accuracy of predictions
    """

    def __init__(self, root_dir, folder_name, gt_dir):
        """
        Args:
            root_dir: Directory to root of the project
            folder_name: Directory from the folder in the annotated map
            gt_dir:  Directory from the folder to the place where gt.txt is stored
        """
        self.root_dir = root_dir
        self.folder_name = folder_name
        self.gt_dir = gt_dir
        self.images_dir = f'{root_dir}/data/annotated/{folder_name}/img1-complete'
        self.results = {}
        self.image_width = 0
        self.image_height = 0

        bounding_boxes_path_gt = f'{root_dir}/data/annotated/{folder_name}/{gt_dir}'

        self.bounding_boxes_gt = self.read_boxes(self.images_dir, bounding_boxes_path_gt)

        configs = configparser.ConfigParser(allow_no_value=True)
        configs.read(f'{root_dir}/configs.ini')
        yolo_config = configs['Yolov5']

        self.iou_threshold = float(yolo_config['iou-thres'])

    def parse_boxes(self, boxes_to_parse):
        """
        Args:
            boxes_to_parse: A list of list of bounding boxes

        Returns:
            A list of bounding boxes as specified by the podm.podm library
        """
        list_parsed_boxes: List[BoundingBox] = []
        for i in enumerate(boxes_to_parse):
            boxes = boxes_to_parse[i[0]]
            for box in boxes:
                width = box.rectangle[2]
                height = box.rectangle[3]
                parsed_box = BoundingBox(label="undefined", xtl=box.rectangle[0] / self.image_width,
                                         ytl=box.rectangle[1] / self.image_height, xbr=width / self.image_width,
                                         ybr=height / self.image_height, image_name=str(i[0]), score=box.certainty)
                list_parsed_boxes.append(parsed_box)
        return list_parsed_boxes

    def read_boxes(self, dir_image, path_to_boxes):
        """A method for reading the bounding boxes with the pre_annotations.
        Args:
            dir_image: The directory to the image.
            path_to_boxes: Path to the file where the boxes are stored.
        Returns:
            A list of bounding boxes.
        """
        capture = ImageCapture(dir_image)
        self.image_width = capture.image_shape[0]
        self.image_height = capture.image_shape[1]
        bounding_boxes_annotations = PreAnnotations(path_to_boxes, capture.nr_images)
        bounding_boxes_annotations.parse_file()
        bounding_boxes = bounding_boxes_annotations.boxes
        return self.parse_boxes(bounding_boxes)

    def detect(self, det_dir):
        """
        Args:
            det_dir: The directory to the file for detections
            (directory from the folder specified when the object was initialized)
        Returns:
            This method currently has no returns.
        """
        bounding_boxes_path_mock = f'{self.root_dir}/data/annotated/{self.folder_name}/{det_dir}'
        bounding_boxes_det = self.read_boxes(self.images_dir, bounding_boxes_path_mock)

        self.results = get_pascal_voc_metrics(self.bounding_boxes_gt, bounding_boxes_det, self.iou_threshold)

        tps = 0
        for value in self.results.values():
            tps += value.tp

        print("tp (all classes): " + str(tps))
        print("tp (only undefined): " + str(self.results['undefined'].tp))
        print("fp: " + str(self.results['undefined'].fp))
        print("fns:" + str(len(self.bounding_boxes_gt) - self.results['undefined'].tp))
        print("mAP: " + str(self.results['undefined'].get_mAP(self.results)))

    def draw_pr_plot(self, result, file_prefix):
        """Draw a pr plot of a class.

        Args:
            result: A MetricPerClass object from the PODM library.
            file_prefix: String that is part of the name of the pr image.

        Returns: An image file in the plots folder called file_prefix-result.class

        """
        try:
            plot_precision_recall_curve(result,
                                        f'{self.root_dir}/processor/training/detection/plots/{file_prefix}'
                                        f'-{result.label}')
        except RuntimeError:
            print(f'{file_prefix}-{result.label}: Cannot plot')

    def draw_all_pr_plots(self, file_prefix):
        """Draws the pr plots for all classes in the (podm) result.

        Args:
            file_prefix: String that is part of the name of the pr image.

        Returns: An image file for each class in the plots folder called file_prefix-result.class

        """
        for result in self.results.items():
            self.draw_pr_plot(result[1], file_prefix)


# TEMPORARY, this is used to call the class and to test it
dir_to_root = os.path.abspath(__file__ + '/../../../../')
accuracy_object = AccuracyObject(dir_to_root, 'test', 'gt/gt.txt')
accuracy_object.detect('det/testfile.txt')
accuracy_object.draw_all_pr_plots('800frames-11point')
