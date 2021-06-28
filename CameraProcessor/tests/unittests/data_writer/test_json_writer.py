"""Tests JsonDataWriter class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os.path

from tests.conftest import root_path
from processor.data_writer.json_data_writer import JsonDataWriter


class TestJsonDataWriter:
    """Class for testing the MOT DataWriter."""

    def test_writer(self, bounding_boxes_object_dict):
        """A function that tests all the functionality of the json DataWriter.

        Args:
            bounding_boxes_object_dict ({image_id: BoundingBoxes}): A dict containing bounding_boxes.

        Returns:

        """
        written_file = self.write(bounding_boxes_object_dict)
        self.written_correctly(written_file)

    @staticmethod
    def write(bboxes_dict):
        """Method for writing all detections to the file using the json datawriter.

        Args:
            bboxes_dict ({image_id: BoundingBoxes}): A dict containing bounding_boxes.

        Returns:
            A file where the detections are written to.

        """
        dest_path = os.path.realpath(os.path.join(root_path, 'data', 'tests',
                                                  'unittests', 'data_writer_tests', 'json_data_writer'))
        data_writer = JsonDataWriter(dest_path)
        for key in bboxes_dict.keys():
            data_writer.write(bboxes_dict[key], [1, 1])
        data_writer.close()
        written_file = open(dest_path + '.json', 'r')
        return written_file

    @staticmethod
    def written_correctly(file):
        """Test if the contents of the file are written correctly.

        Args:
            file: A file containing the written detections/tracks.

        """
        first_line = file.readline()
        string_1 = '{"imageId": "13", "boxes": [{"boxId": 78, "rect": [0.1, 0.23, 0.5, 0.4]'
        string_2 = ', "objectType": "car", "certainty": 0.75, "objectId": 18}'
        string = string_1 + string_2
        assert first_line.startswith(string)
