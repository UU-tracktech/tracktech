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

from processor.training.pre_annotations import PreAnnotations

class AccuracyObject:
    """
    This class is used to test the accuracy of predictions
    """

    def __init__(self):
        # Initializing class variables
        self.gt_path = ''
        self.det_path = ''
        self.det_info_path = ''
        self.results = {}
        self.image_width = 10000
        self.image_height = 10000
        self.iou_threshold = 0

        #Assign class variables from config
        self.read_configs()

        # Getting the bounding boxes from the gt file
        self.bounding_boxes_gt = self.read_boxes(self.gt_path)



    def read_configs(self):
        """Assign class variables using the Accuracy and Yolov5 configs
        """
        # Load the config file, take the relevant Accuracy & Yolov5 section
        path_to_root = '../../..'
        configs = configparser.ConfigParser(allow_no_value=True)
        configs.read(path_to_root + '/configs.ini')
        accuracy_config = configs['Accuracy']
        yolo_config = configs['Yolov5']

        self.gt_path = os.path.join(path_to_root, accuracy_config['gt-path'])
        self.det_path = os.path.join(path_to_root, accuracy_config['det-path'])
        self.det_info_path = os.path.join(path_to_root, accuracy_config['det-info-path'])

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

            # Getting the boundingboxes that are detected in frame i

            boxes = boxes_to_parse[i[0]]

            # Parse every boundingbox into a boundingbox from the podm.podm library

            for box in boxes:

                # Parse a single box and append it to the list of already parsed boxes

                width = box.rectangle[2]
                height = box.rectangle[3]
                parsed_box = BoundingBox(label="undefined", xtl=box.rectangle[0] / self.image_width,
                                         ytl=box.rectangle[1] / self.image_height, xbr=width / self.image_width,
                                         ybr=height / self.image_height, image_name=str(i[0]), score=box.certainty)
                list_parsed_boxes.append(parsed_box)
        return list_parsed_boxes

    def read_boxes(self, path_to_boxes):
        """A method for reading the bounding boxes with the pre_annotations.
        Args:
            path_to_boxes: Path to the file where the boxes are stored.
        Returns:
            A list of bounding boxes.
        """
        # Using the PreAnnotations class to get the boundingboxes from a file
        bounding_boxes_annotations = PreAnnotations(path_to_boxes, 836)
        bounding_boxes_annotations.parse_file()
        bounding_boxes = bounding_boxes_annotations.boxes
        return self.parse_boxes(bounding_boxes)

    def detect(self):
        """
        Args:
            det_dir: The directory to the file for detections
            (directory from the folder specified when the object was initialized)
        Returns:
            This method currently has no returns.
        """

        # Getting and parsing the boundingboxes from the detection file
        bounding_boxes_det = self.read_boxes(self.det_path)

        # Using the podm.podm library to get the accuracy metrics
        self.results = get_pascal_voc_metrics(self.bounding_boxes_gt, bounding_boxes_det, self.iou_threshold)

        # Printing a few metrics related to accuracy on the terminal

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


test_object = AccuracyObject()
test_object.detect()
