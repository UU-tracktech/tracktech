import os
from tests.unittests.preannotations.test_pre_annotations import example_json_file
from src.training.pre_annotations import PreAnnotations


# pylint: disable=attribute-defined-outside-init
class TestJsonParsing:
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
        """Test parsing of a json file that correct rectangles are generated.
        """
        self.annotations.parse_json_file()
        first_box = self.annotations.boxes[0][0]
        second_box = self.annotations.boxes[1][0]
        assert first_box.rectangle == [1127, 100, 1165, 268]
        assert first_box.identifier == 1
        assert second_box.rectangle == [1127, 103, 1165, 271]
        assert second_box.identifier == 1

    def test_line_skipping(self):
        """Tests whether the pre annotations skips lines of frames that are beyond the number of frames given
        """
        self.short_annotations.parse_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.short_annotations.boxes]
        print(number_boxes)
        assert self.short_annotations.skipped_lines == 4
        assert number_boxes == [1, 1]
