"""MOT dataloader class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import logging
from os import path

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.dataloaders.i_dataloader import IDataloader


class MotDataloader(IDataloader):
    """MOT Dataloader, formats MOT Data."""

    def __init__(self, configs, path_location):
        """Initializes the MOTDataloader.

        Args:
            configs (dict): Configurations containing settings for dataloader.
            path_location (str): The path of the MOT data.
        """
        super().__init__(configs, path_location)
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
            image_id (int): Id of the image.

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
        if image_id in self.image_dimensions:
            return self.image_dimensions[image_id]
        image_name = self.__get_image_name(image_id)
        this_image_path = self.__get_image_path(image_name)
        image = Image.open(this_image_path)
        self.image_dimensions[image_id] = image.size
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
        pos_y-= 1
        width, height = self.get_image_dimensions(image_id)
        return_values = (image_id, identifier, pos_x / width, pos_y / height, (pos_x + pos_w) / width,
                         (pos_y + pos_h) / height, certainty, None, None)
        return [return_values]
