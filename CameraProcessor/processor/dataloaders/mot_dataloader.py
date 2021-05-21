"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import logging
from os import path
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.utils.config_parser import ConfigParser


class IDataloader:



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
            annotations.append((image_id,person_id,pos_x,pos_y,pos_w,pos_h))
        return annotations

    def __parse_boxes(self, annotations):
        boxes = []
        # Extract information from lines
        for annotation in annotations:
            (image_id, person_id, pos_x, pos_y, pos_w, pos_h) = annotation
            boxes.append(BoundingBox(classification='person',
                                     rectangle=Rectangle(x1=pos_x,
                                                         y1=pos_y,
                                                         x2=(pos_x + pos_w),
                                                         y2=(pos_y + pos_h),
                                                         identifier=person_id,
                                                         certainty=1)))
        return boxes

    def __log_skipped(self):
        # Logs when lines skipped
        if self.skipped_lines > 0:
            logging.info(f'Skipped lines: {self.skipped_lines}')

    def parse_file(self):
        annotations = self.__get_annotations()
        self.__log_skipped()
        boxes = self.__parse_boxes(annotations)
        return BoundingBox(boxes)

    def __get_image_path(self, image_id):
        zeros = ''
        for i in range(6 - len(str(image_id))):
            zeros += '0'
        this_image_path = path.abspath(f'{self.image_path}/{zeros}{image_id}.jpg')
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
