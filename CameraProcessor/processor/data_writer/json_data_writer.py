"""Datawriter implementation for JSON.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from processor.data_writer.i_data_writer import IDataWriter
from processor.utils.text import boxes_to_accuracy_json
import os


class JsonDataWriter(IDataWriter):
    """Data Writer implementation for JSON"""
    def __init__(self, det_destination):
        """Initializing the JSON data writer"""
        super().__init__()
        destination_file = os.path.realpath(det_destination + '.json')
        self.file = open(destination_file, 'w')

    def write(self, bounding_boxes, shape):
        """Method for saving the data to write later.

        Args:
            bounding_boxes (BoundingBoxes): An object containing the bounding boxes that need to be written.
            shape (int, int): A tuple containing the width and height of the frames.
        """
        # Getting the string to write to the json file.
        image_id = bounding_boxes.image_id
        string_to_write = boxes_to_accuracy_json(bounding_boxes, image_id)

        # Writing to the file.
        try:
            self.file.write(f'{string_to_write}\n')
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')

    def close(self):
        """Method for closing the JSON Data Writer"""
        self.file.close()
