"""Tests whether pre_annotations are correctly loaded in from a json file

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
from tests.unittests.training.test_pre_annotations import example_json_file
from processor.training.pre_annotations import PreAnnotations
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init
class TestJsonParsing:
    """Checks whether the json file is parsed in a correct way

    """
    def setup_method(self) -> None:
        """Sets up an annotations object that can be parsed.
        """
        self.annotations = PreAnnotations(example_json_file, 6)
        self.short_annotations = PreAnnotations(example_json_file, 2)

    def test_file_exists(self) -> None:
        """Checks whether test file exists.
        """
        assert os.path.exists(example_json_file)

    def test_file_parsing(self) -> None:
        """Test parsing of the text file and compares the number of boxes found
        with the expected number.
        """
        self.annotations.parse_json_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.annotations.boxes]
        expected = [1, 1, 1, 1, 1, 1]
        assert number_boxes == expected

    def test_json_parsing(self) -> None:
        """Test parsing of a json file that correct rectangle is generated.
        """
        self.annotations.parse_json_file()
        bounding_box = self.annotations.boxes[0][0]
        result = bounding_box.get_rectangle()
        expected = Rectangle(1127, 100, 1165, 268)

        # The coordinates are loaded in correctly
        assert result.get_x1() == expected.get_x1()
        assert result.get_y1() == expected.get_y1()
        assert result.get_x2() == expected.get_x2()
        assert result.get_y2() == expected.get_y2()

    def test_line_skipping(self):
        """Tests whether the pre annotations skips lines of frames that are beyond the number of frames given
        """
        self.short_annotations.parse_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.short_annotations.boxes]
        print(number_boxes)
        assert self.short_annotations.skipped_lines == 4
        assert number_boxes == [1, 1]
