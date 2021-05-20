"""Dataloader super class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import logging

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.utils.config_parser import ConfigParser


class IDataloader:

    def get_image_dimensions(self, image_id):
        """Gets the size of an image based on its name.

        Args:
            image_id: String with the name of the image.

        Returns: width, height (integers).

        """
        raise NotImplementedError('get image size method not implemented')

    def parse_file(self):
        # Read file
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        # Determine delimiter automatically
        delimiter = ' '
        if lines[0].__contains__(','):
            delimiter = ','

        boxes = []
        # Extract information from lines
        for line in lines:
            (frame_nr, person_id, pos_x, pos_y, pos_w, pos_h) = self.parse_line(line, delimiter)
            if frame_nr - 1 >= self.nr_frames:
                self.skipped_lines = self.skipped_lines + 1
                continue

            # Create bounding box
            rectangle = Rectangle(
                pos_x, pos_y,
                (pos_x + pos_w), (pos_y + pos_h)
            )
            # Append box to list of boxes
            box = BoundingBox(person_id, rectangle, "UFO", 1)
            self.boxes[frame_nr - 1].append(box)

        # Logs when lines skipped
        if self.skipped_lines > 0:
            logging.info(f'Skipped lines: {self.skipped_lines}')

    @staticmethod
    def parse_line(line, delimiter):
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
