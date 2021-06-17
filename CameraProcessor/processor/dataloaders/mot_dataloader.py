"""MOT dataloader class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import logging
from os import path
from PIL import Image

from processor.dataloaders.i_dataloader import IDataloader


class MotDataloader(IDataloader):
    """MOT Dataloader, formats MOT Data."""

    def __init__(self, configs):
        """Initializes the MOTDataloader.

        Args:
            configs (dict): Configurations containing settings for dataloader.
        """
        super().__init__(configs)
        dataloader_config = configs['MOT']
        self.file_path = dataloader_config['annotations_path']
        self.image_path = dataloader_config['image_path']
        self.image_dimensions = (-1, -1)
        self.skipped_lines = []
        self.delimiter = ' '

    def get_annotations(self):
        """Gets annotations.

        Returns:
            annotations (list): List of string annotations.
        """
        # Read file.
        with open(self.file_path) as file:
            lines = [line.rstrip('\n') for line in file]

        # Determine delimiter automatically.
        if lines[0].__contains__(','):
            self.delimiter = ','

        return lines

    def __log_skipped(self):
        """Logs when lines skipped."""
        if self.skipped_lines:
            logging.info(f'Skipped lines: {self.skipped_lines}')

    @staticmethod
    def __get_image_name(image_id):
        """Get the name of an image.

        Args:
            image_id (int): ID of the image.

        Returns:
            name (string): Properly formatted image id.
        """
        zeros = ''
        for _ in range(6 - len(str(image_id))):
            zeros += '0'
        name = f'{zeros}{image_id}'
        return name

    def __get_image_path(self, image_id):
        """Converts the image id to a proper filepath.

        Args:
            image_id (int): The id of an image.

        Returns:
            (string): Filepath to the image.
        """
        image_name = self.__get_image_name(image_id)
        this_image_path = path.abspath(f'{self.image_path}/{image_name}.jpg')
        return this_image_path

    def get_image_dimensions(self, image_id):
        """Gets the size of an image based on its name.

        Args:
            image_id (integer): String with the name of the image.

        Returns:
            (int,int): width and height dimensions of the image.
        """
        if self.image_dimensions >= (0, 0):
            return self.image_dimensions[image_id]
        image_name = self.__get_image_name(image_id)
        this_image_path = self.__get_image_path(image_name)

        # File did not exist.
        if not os.path.exists(this_image_path):
            return None, None

        # Open image and return its size.
        image = Image.open(this_image_path)
        self.image_dimensions = image.size
        return image.size

    def parse_line(self, line):
        """Parse line from file given a delimiter.

        Args:
            line (str): line in file.

        Returns:
            list (list): List of integer values of line parsed and put inside string.
        """
        (image_id, identifier, pos_x, pos_y, pos_w, pos_h, certainty) = [int(i) for i in line.split(self.delimiter)[:7]]
        # MOT is 1 based, while this project is 0 based.
        pos_x -= 1
        pos_y -= 1
        width, height = self.get_image_dimensions(image_id)

        # Image did not exist.
        if width is None or height is None:
            return []

        # Make sure values are between the frame borders.
        pos_x1 = max(pos_x, 0)
        pos_y1 = max(pos_y, 0)
        box_x2 = min(pos_x + pos_w, width)
        box_y2 = min(pos_y + pos_h, height)

        return [(image_id, identifier, pos_x1 / width, pos_y1 / height, box_x2 / width,
                box_y2 / height, certainty, '', None)]
