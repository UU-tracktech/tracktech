"""File containing the accuracy class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import time

from podm.podm import BoundingBox, get_pascal_voc_metrics
from podm.visualize import plot_precision_recall_curve

from processor.utils.dataloader import get_dataloader
from processor.utils.config_parser import ConfigParser


class AccuracyObject:
    """This class is used to test the accuracy of predictions.

    Attributes:
        results (object): Results of the PODM library.
        iou_threshold (int): Threshold from which it is counted.
        frame_amount (int): Number of frames.
        gt_format (str): Format of the ground truth.
        plots_prefix (str): Prefix of the name of a plot.
        plots_path (str): Path where to create plots.
        configs (dict): The configs as a dictionary.
        bounding_boxes_gt ([BoundingBox]):
    """

    def __init__(self, configs):
        """Initialise AccuracyObject by reading the config, and the ground truth file.

        Args:
            configs (Dict): Configuration parser, which also contains the accuracy configurations.
        """
        yolo_config = configs['Yolov5']
        accuracy_config = configs['Accuracy']
        # Currently unused: coco_config = configs['COCO'].
        # Initializing class variables.
        self.results = {}
        self.iou_threshold = float(yolo_config['iou-thres'])
        self.frame_amount = int(accuracy_config['nr_frames'])
        self.gt_format = accuracy_config['gt_format']
        self.det_format = accuracy_config['det_format']
        gt_dataloader_config = configs[self.gt_format]
        self.plots_prefix = accuracy_config['plots_prefix']
        self.plots_path = gt_dataloader_config['plots_path']
        self.configs = configs
        self.bounding_boxes_gt = []

    def parse_boxes(self, boxes_to_parse):
        """Parse boxes to PODM format.

        Args:
            boxes_to_parse (Dict): A dict of BoundingBoxes objects with image ids as keys.

        Returns:
            [BoundingBox]: A list of bounding boxes as specified by the podm.podm library.
        """
        list_parsed_boxes = []
        for bounding_boxes_object in boxes_to_parse.values():

            # Getting the bounding boxes that are detected in frame i.
            image_id = bounding_boxes_object.image_id

            # Parse every bounding box into a bounding box from the podm.podm library.

            for box in bounding_boxes_object.bounding_boxes:
                # Parse a single box and append it to the list of already parsed boxes.
                # The label is currently undefined because class information is not yet saved.
                parsed_box = BoundingBox(
                    label=box.classification,
                    xtl=box.rectangle.x1,
                    ytl=box.rectangle.y1,
                    xbr=box.rectangle.x2,
                    ybr=box.rectangle.y2,
                    image_name=str(image_id),
                    score=box.certainty
                )
                list_parsed_boxes.append(parsed_box)
        return list_parsed_boxes

    def read_boxes(self, annotation_format):
        """A method for reading the bounding boxes with the pre_annotations.

        Args:
            annotation_format (str): String format of annotation.

        Returns:
            [BoundingBoxes]: A list of read bounding boxes.
        """
        dataloader = get_dataloader(self.configs, annotation_format)
        bounding_boxes_objects = dataloader.parse_file()
        return self.parse_boxes(bounding_boxes_objects)

    def detect(self):
        """Retrieves accuracy of detections."""
        print("Start accuracy calculations.")

        print("Parsing the ground truth.")
        # Getting the bounding boxes from the gt file.
        self.bounding_boxes_gt = self.read_boxes(self.gt_format)

        print("Parsing the detections.")
        # Getting and parsing the bounding boxes from the detection file.
        bounding_boxes_det = self.read_boxes('JSON')

        print("Calculating the AP.")
        # Using the podm.podm library to get the accuracy metrics.
        self.results = get_pascal_voc_metrics(
            self.bounding_boxes_gt,
            bounding_boxes_det,
            self.iou_threshold
        )

        # Printing a few metrics related to accuracy on the terminal.
        # Labels are undefined because the det and gt files currently don't save the classes of detected objects.
        # Pprint("tp (only undefined): " + str(self.results['undefined'].tp)).
        # Pprint("fp: " + str(self.results['undefined'].fp)).
        # Pprint("fns:" + str(len(self.bounding_boxes_gt) - self.results['undefined'].tp)).
        # Pprint("mAP: " + str(self.results['undefined'].get_mAP(self.results))).

    def draw_pr_plot(self, result):
        """Draw a pr plot of a class and saves it to a file.

        Args:
            result (MetricPerClass): A MetricPerClass object from the PODM library.
        """
        try:
            os.makedirs(self.plots_path, exist_ok=True)
            plot_precision_recall_curve(result,
                                        os.path.join(self.plots_path,
                                                     f'{time.strftime("%Y-%m-%d_%H-%M-%S")}-'
                                                     f'{self.plots_prefix}-'
                                                     f'{result.label}')
                                        )
        except RuntimeError:
            print(f'{self.plots_prefix}-{result.label}: Cannot plot')

    def draw_all_pr_plots(self):
        """Draws the pr plots for all classes in the PODM result."""
        for result in self.results.items():
            if result[1].num_detection != 0:
                self.draw_pr_plot(result[1])


if __name__ == '__main__':
    # Run accuracy.
    config_parser = ConfigParser('configs.ini', True)
    test_object = AccuracyObject(config_parser.configs)

    # Detect and plot all the information.
    test_object.detect()
    test_object.draw_all_pr_plots()
