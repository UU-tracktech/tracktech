"""This test file tests if the output of the accuracy_runner is in the correct format.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import json

from processor.accuracy_runner import main


# pylint: disable=attribute-defined-outside-init
class TestAccuracyRunner:
    """Test if the accuracy outputs information in the correct format.

    Attributes:
        config_accuracy (SectionProxy): Accuracy section of the test configurations.
    """

    def test_accuracy_runner(self, configs):
        """Runs the accuracy runner and gets the correct paths from the config file.

        Args:
            configs (ConfigParser): configs for the test.
        """
        # Run the accuracy runner.
        main(configs)

        # Getting the config file for the accuracy.
        self.config_accuracy = configs['Accuracy']
        self.detection_file()

    def detection_file(self):
        """Tests if the information in the detection file is correct and within the logical bounds."""
        # Opening and reading file.
        file = open(self.config_accuracy['det_path'], 'r')
        lines = file.readlines()
        file.close()

        for line in lines:
            json_line = json.loads(line)
            assert len(json_line['imageId']) > 0
            boxes = json_line['boxes']
            assert len(boxes) > 0
            for box in boxes:
                assert int(box['boxId']) >= 0
                assert 1 > float(box['certainty']) >= 0
                assert len(str(box['objectType'])) > 0
                assert 1 >= float(box['rect'][0]) >= 0
                assert 1 >= float(box['rect'][1]) >= 0
                assert 1 >= float(box['rect'][2]) >= 0
                assert 1 >= float(box['rect'][3]) >= 0

    def tracking_file(self):
        """Tests if the information in the tracking file is correct and within the logical bounds."""
        # Opening and reading file.
        file = open(self.config_accuracy['det_path'], 'r')
        lines = file.readlines()
        file.close()

        # Getting picture information from the detection info.
        file_info = open(self.config_accuracy['det-info_path'], 'r')
        line_info = file_info.readline()
        file_info.close()
        image_width = int(line_info.split(",")[1])
        image_height = int(line_info.split(",")[2])

        # Checking if the information in every line is in line with the guidelines for the first 6 values.
        # These are defined in https://motchallenge.net/instructions/.
        previous_frame_nr = 0
        previous_id = 0
        for line in lines:
            (frame_nr, person_id, pos_x, pos_y, pos_w, pos_h) = line.split(",")[:6]
            assert int(frame_nr) >= previous_frame_nr
            assert int(person_id) > previous_id or int(person_id) == 0
            assert 0 <= int(pos_x) <= int(pos_x) + int(pos_w) <= image_width
            assert 0 <= int(pos_y) <= int(pos_y) + int(pos_h) <= image_height
