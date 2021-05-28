"""File containing the accuracy class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import time
from podm.podm import BoundingBox, get_pascal_voc_metrics
from podm.visualize import plot_precision_recall_curve

from processor.dataloaders.coco_dataloader import COCODataloader
from processor.dataloaders.json_dataloader import JSONDataloader
from processor.dataloaders.mot_dataloader import MOTDataloader
from processor.training.pre_annotations import PreAnnotations
from processor.utils.config_parser import ConfigParser


class AccuracyObject:
    """This class is used to test the accuracy of predictions."""

    def __init__(self, configs):
        """Initialise AccuracyObject by reading the config and the ground truth file."""
        # Initializing class variables
        self.results = {}
        self.image_width = 0
        self.image_height = 0
        self.iou_threshold = 0
        self.frame_amount = 0

        # Assign class variables from config
        self.read_config(configs)
        self.configs = configs

        self.bounding_boxes_gt = []

    def read_config(self, configs):
        """Assign class variables using the Accuracy config."""
        # Load the config file, take the relevant Accuracy section
        self.yolo_config = configs['Yolov5']
        self.accuracy_config = configs['Accuracy']

    def parse_info_file(self):
        """Reads frame height, width and the amount of frames from the info file."""
        with open(self.accuracy_config['det-info_path'], 'r') as file:
            lines = [line.rstrip('\n') for line in file]

        line = lines[0]

        # Determine delimiter automatically
        if line.__contains__(','):
            delimiter = ','
        else:
            return

        # Extract information from line
        (self.frame_amount, self.image_width, self.image_height) = [int(i) for i in line.split(delimiter)[:3]]

    def parse_boxes(self, boxes_to_parse):
        """Parses boxes to podm format.

        Args:
            boxes_to_parse: A list of list of bounding boxes.

        Returns:
            A list of bounding boxes as specified by the podm.podm library.

        """
        list_parsed_boxes = []
        for i in enumerate(boxes_to_parse):

            # Getting the bounding boxes that are detected in frame i

            boxes = boxes_to_parse[i[0]]

            # Parse every bounding box into a bounding box from the podm.podm library

            for box in boxes:
                # Parse a single box and append it to the list of already parsed boxes
                # The label is currently undefined because class information is not yet saved.
                parsed_box = BoundingBox(
                    label="undefined",
                    xtl=box.get_rectangle().get_x1(),
                    ytl=box.get_rectangle().get_y1(),
                    xbr=box.get_rectangle().get_x2(),
                    ybr=box.get_rectangle().get_y2(),
                    image_name=str(i[0]),
                    score=box.get_certainty()
                )
                list_parsed_boxes.append(parsed_box)
        return list_parsed_boxes

    def get_dataloader(self, type, path_location):
        switch = {
            "COCO": COCODataloader(self.configs, path_location),
            "JSON": JSONDataloader(self.configs, path_location),
            "MOT": MOTDataloader(self.configs, path_location)
        }
        return switch.get(type, ValueError("This is not a valid dataloader"))

    def read_boxes(self, type, path_location):
        """A method for reading the bounding boxes with the pre_annotations.

        Args:
            path_location: Path to the file where the boxes are stored.

        Returns:
            A list of bounding boxes.
        """
        dataloader = self.get_dataloader(type, path_location)
        bounding_boxes_objects = dataloader.parse_file()
        bounding_boxes = []
        for bounding_boxes_object in bounding_boxes_objects:
            bounding_boxes.append(bounding_boxes_object.get_bounding_boxes())
        return self.parse_boxes(bounding_boxes)

    def detect(self):
        """Retrieves accuracy of detections.

        Args:
            (directory from the folder specified when the object was initialized).
        Returns:
            This method currently has no returns.
        """

        # Getting the bounding boxes from the gt file
        self.bounding_boxes_gt = self.read_boxes(self.accuracy_config['det_format'], 'gt_path')

        # Getting and parsing the bounding boxes from the detection file
        bounding_boxes_det = self.read_boxes('JSON', 'det_path')

        # Using the podm.podm library to get the accuracy metrics
        self.results = get_pascal_voc_metrics(
            self.bounding_boxes_gt,
            bounding_boxes_det,
            float(self.yolo_config['iou-thres'])
        )

        # Printing a few metrics related to accuracy on the terminal, labels are undefined because the det and
        # gt files currently don't save the classes of detected objects
        print("tp (only undefined): " + str(self.results['undefined'].tp))
        print("fp: " + str(self.results['undefined'].fp))
        print("fns:" + str(len(self.bounding_boxes_gt) - self.results['undefined'].tp))
        print("mAP: " + str(self.results['undefined'].get_mAP(self.results)))

    def draw_pr_plot(self, result):
        """Draw a pr plot of a class.

        Args:
            result: A MetricPerClass object from the PODM library.

        Returns: An image file in the plots folder called file_prefix-result.class.
        """
        try:
            os.makedirs(self.accuracy_config['plots_path'], exist_ok=True)
            plot_precision_recall_curve(result,
                                        os.path.join(self.accuracy_config['plots_path'],
                                                     f'{time.strftime("%Y-%m-%d_%H-%M-%S")}-'
                                                     f'{self.accuracy_config["plots_prefix"]}-'
                                                     f'{result.label}')
                                        )
        except RuntimeError:
            print(f'{self.accuracy_config["plots_prefix"]}-{result.label}: Cannot plot')

    def draw_all_pr_plots(self):
        """Draws the pr plots for all classes in the (podm) result.

        Returns: An image file for each class in the plots folder called file_prefix-result.class.
        """
        for result in self.results.items():
            self.draw_pr_plot(result[1])


if __name__ == "__main__":
    config_parser = ConfigParser('configs.ini')
    test_object = AccuracyObject(config_parser.configs)
    test_object.detect()
    test_object.draw_all_pr_plots()
