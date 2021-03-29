import os
from test_pre_annotations import example_text_file
from src.training.pre_annotations import PreAnnotations

class TestTextParsing:
    def setup_method(self):
        self.annotations = PreAnnotations(example_text_file, 5)

    def test_file_exists(self):
        assert os.path.exists(example_text_file)

    def test_file_parsing(self):
        self.annotations.parse_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.annotations.boxes]
        expected = [1, 2, 2, 1, 1]
        assert number_boxes == expected

    def test_comma_line_parsing(self):
        with open(example_text_file) as file:
            first_line = [line.rstrip('\n') for line in file][0]
        information = self.annotations.parse_line(first_line, ',')
        assert information == [1, 1, 17, 150, 77, 191]

    def test_line_parsing(self):
        with open(example_text_file) as file:
            first_line = [line.rstrip('\n') for line in file][0]
        first_line.replace(',', ' ')
        information = self.annotations.parse_line(first_line, ',')
        assert information == [1, 1, 17, 150, 77, 191]
