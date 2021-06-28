"""Tests MotDataWriter class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os.path

from tests.conftest import root_path
from processor.data_writer.mot_data_writer import MotDataWriter


class TestMotDataWriter:
    """Class for testing the MOT DataWriter."""
    def test_writer(self, bounding_boxes_object_dict):
        """A function that tests all the functionality of the MOT DataWriter

        Args:
            bounding_boxes_object_dict ({image_id: BoundingBoxes}): A dict containing bounding_boxes

        Returns:

        """
        written_file = self.write(bounding_boxes_object_dict)
        self.written_correctly(written_file)

    @staticmethod
    def write(bboxes_dict):
        """Method for writing all detections to the file using the MOT datawriter.

        Args:
            bboxes_dict ({image_id: BoundingBoxes}): A dict containing bounding_boxes.

        Returns:
            A file where the detections are written to.

        """
        dest_path = os.path.realpath(os.path.join(root_path, 'data', 'tests',
                                                  'unittests', 'data_writer_tests', 'mot_data_writer'))
        data_writer = MotDataWriter(dest_path)
        for key in bboxes_dict.keys():
            data_writer.write(bboxes_dict[key], [1, 1])
        data_writer.close()
        written_file = open(dest_path + '.txt', 'r')
        return written_file

    @staticmethod
    def written_correctly(file):
        """Test if the contents of the file are written correctly

        Args:
            file: A file containing the written detections/tracks.

        """
        old_object_id = -1
        old_frame_id = -1
        for line in file.readlines():
            frame_id = int(line.split(',')[0])
            object_id = int(line.split(',')[1])
            assert object_id > old_object_id or frame_id > old_frame_id
            old_frame_id = frame_id
            old_object_id = object_id
