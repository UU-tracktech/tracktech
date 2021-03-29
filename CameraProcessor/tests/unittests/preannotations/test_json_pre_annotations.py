import os
from test_pre_annotations import example_json_file
from src.training.pre_annotations import PreAnnotations


class TestJsonParsing:
    def setup_method(self):
        self.annotations = PreAnnotations(example_json_file, 6)

    def test_file_exists(self):
        assert os.path.exists(example_json_file)

    def test_file_parsing(self):
        self.annotations.parse_json_file()
        number_boxes = [len(boxes_frame) for boxes_frame in self.annotations.boxes]
        expected = [1, 1, 1, 1, 1, 1]
        assert number_boxes == expected

    def test_object_parsing(self):
        self.annotations.parse_json_file()
        print(self.annotations.boxes)

    def test_json_parsing(self):
        pass
