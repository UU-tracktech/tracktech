"""Tests whether pre_annotations are correctly loaded in from a text file

"""
import os
import pytest
from processor.training.pre_annotations import PreAnnotations
from tests.unittests.preannotations.test_pre_annotations import example_text_file


# pylint: disable=attribute-defined-outside-init
class TestTextParsing:
    """Tests the parsing of text files, these contain the bounding boxes of subjects
    """
    def setup_method(self) -> None:
        """Creates pre annotations object that contains information for 5 frames
        """
        self.annotations = PreAnnotations(example_text_file, 5)
        self.short_annotations = PreAnnotations(example_text_file, 2)

    def test_file_exists(self) -> None:
        """Checks whether test file exists
        """
        assert os.path.exists(example_text_file)

    def test_file_parsing(self) -> None:
        """Parses test file and sees whether the number of boxes match
        """
        self.annotations.parse_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.annotations.boxes]
        expected = [1, 2, 2, 1, 1]
        assert number_boxes == expected

    def test_comma_line_parsing(self) -> None:
        """Using comma as delimiter checks whether line is parsed correctly
        """
        with open(example_text_file) as file:
            first_line = [line.rstrip('\n') for line in file][0]
        information = self.annotations.parse_line(first_line, ',')
        assert information == [1, 1, 17, 150, 77, 191]

    def test_line_parsing(self) -> None:
        """Using space as delimiter checks whether line is parsed correctly
        """
        with open(example_text_file) as file:
            first_line = [line.rstrip('\n') for line in file][0]
        first_line.replace(',', ' ')
        information = self.annotations.parse_line(first_line, ',')
        assert information == [1, 1, 17, 150, 77, 191]

    def test_line_skipping(self):
        """Tests whether the pre annotations skips lines of frames that are beyond the number of frames given
        """
        self.short_annotations.parse_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.short_annotations.boxes]

        assert self.short_annotations.skipped_lines == 4
        assert number_boxes == [1, 2]


if __name__ == '__main__':
    pytest.main(TestTextParsing)
