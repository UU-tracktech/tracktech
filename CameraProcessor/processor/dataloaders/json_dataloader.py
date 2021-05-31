"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.dataloaders.idataloader import IDataloader


class JSONDataloader(IDataloader):
    def parse_file(self):
        """Parses a file into a BoundingBoxes object.

        Returns:
            bounding_boxes_list (list): a BoundingBoxes object.
        """
        annotations = self.__get_annotations()
        bounding_boxes_list = self.__parse_boxes(annotations)
        return bounding_boxes_list

    def __parse_boxes(self, annotations):
        """Parses bounding boxes.

        Args:
            annotations (list): List of strings.

        Returns:
            bounding_boxes_list (list): List of bounding boxes.
        """
        bounding_boxes_list = []
        current_boxes = []
        current_image_id = annotations[0][0]
        # Extract information from lines.
        for annotation in annotations:
            (image_id, person_id, certainty, object_type, pos_x, pos_y, pos_x2, pos_y2) = annotation
            if not current_image_id == image_id:
                bounding_boxes_list.append(BoundingBoxes(current_boxes, current_image_id))
                current_boxes = []
                current_image_id = image_id
            current_boxes.append(BoundingBox(classification='person',
                                             rectangle=Rectangle(x1=pos_x,
                                                                 y1=pos_y,
                                                                 x2=pos_x2,
                                                                 y2=pos_y2),
                                             identifier=person_id,
                                             certainty=certainty))
        return bounding_boxes_list

    def __get_annotations(self):
        # Read file.
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        annotations = []
        # Extract information from lines.
        for line in lines:
            json_line = json.loads(line)
            image_id = json_line['imageId']
            boxes = json_line['boxes']
            for box in boxes:
                person_id = box['boxId']
                certainty = box['certainty']
                object_type = box['objectType']
                x1 = box['rect'][0]
                y1 = box['rect'][1]
                x2 = box['rect'][2]
                y2 = box['rect'][3]
                annotations.append((image_id, person_id, certainty, object_type, x1, y1, x2, y2))
        return annotations
