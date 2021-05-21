"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import logging
from os import path

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.dataloaders.idataloader import IDataloader


class MOTDataloader(IDataloader):

    def __get_annotations(self):
        # Read file
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        # Determine delimiter automatically
        delimiter = ' '
        if lines[0].__contains__(','):
            delimiter = ','

        annotations = []
        # Extract information from lines
        for line in lines:
            (image_id, person_id, pos_x, pos_y, pos_w, pos_h) = self.__parse_line(line, delimiter)
            if image_id - 1 >= self.nr_frames:
                self.skipped_lines = self.skipped_lines + 1
                continue
            annotations.append((image_id, person_id, pos_x, pos_y, pos_w, pos_h))
        return annotations

    def __parse_boxes(self, annotations):
        bounding_boxes_list = []
        current_boxes = []
        current_image_id = annotations[0][0]
        # Extract information from lines
        for annotation in annotations:
            (image_id, person_id, pos_x, pos_y, pos_w, pos_h) = annotation
            this_image_path = self.__get_image_path(image_id)
            width, height = self.get_image_dimensions(image_id, this_image_path)
            if not current_image_id == image_id:
                bounding_boxes_list.append(BoundingBoxes(current_boxes, current_image_id))
                current_boxes = []
                current_image_id = image_id
            current_boxes.append(BoundingBox(classification='person',
                                             rectangle=Rectangle(x1=pos_x / width,
                                                                 y1=pos_y / height,
                                                                 x2=(pos_x + pos_w) / width,
                                                                 y2=(pos_y + pos_h) / height),
                                             identifier=person_id,
                                             certainty=1))
        return bounding_boxes_list

    def __log_skipped(self):
        # Logs when lines skipped
        if self.skipped_lines > 0:
            logging.info(f'Skipped lines: {self.skipped_lines}')

    def parse_file(self):
        annotations = self.__get_annotations()
        self.__log_skipped()
        bounding_boxes_list = self.__parse_boxes(annotations)
        return bounding_boxes_list

    @staticmethod
    def __get_image_name(image_id):
        zeros = ''
        for i in range(6 - len(str(image_id))):
            zeros += '0'
        return f'{zeros}{image_id}.jpg'

    def __get_image_path(self, image_id):
        image_name = self.__get_image_name(image_id)
        this_image_path = path.abspath(f'{self.image_path}/{image_name}')
        return this_image_path

    @staticmethod
    def __parse_line(line, delimiter):
        """Parse line from file given a delimiter.

        First 6 values are
        "<frameID>,<objectID>,<x1>,<y1>,<x2>,<y2>,.. jibberish"

        Args:
            line (str): line in file.
            delimiter (str): delimiter values in line are separated with.

        Returns:
            Integer values of line parsed and put inside string.
        """
        return [int(i) for i in line.split(delimiter)[:6]]
