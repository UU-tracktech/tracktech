"""This test file tests if the output of the accuracy_runner is in the correct format.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

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

        # Test the files created by the accuracy runner.
        self.detection_info_file()
        self.detection_file()

    def detection_info_file(self):
        """Tests if the information in the detection file is correctly formatted and possible."""
        # Opening and reading file.
        file = open(self.config_accuracy['det-info_path'], 'r')
        lines = file.readlines()
        line = lines[0]
        file.close()

        # Making sure the file only contains one line.
        assert len(lines) == 1

        # Check if the line has a correct number of arguments.
        args = line.split(",")
        assert len(args) == 3

        # Check if the arguments them selves have logical values.
        # Check if the number of frames is strictly bigger than 0.
        assert int(args[0]) > 0

        # Check if the image height is correct and logical.
        assert 10000 > int(args[1]) > 0

        # Check if the image width is correct and logical.
        assert 10000 > int(args[2]) > 0

    def detection_file(self):
        """Tests if the information in the detection file is correct and within the logical bounds."""
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
