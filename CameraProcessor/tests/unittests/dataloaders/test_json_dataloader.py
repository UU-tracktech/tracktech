"""Tests the JSON dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.json_dataloader import JsonDataloader


# pylint: disable=attribute-defined-outside-init
class TestJsonDataloader:
    """Tests the JSON dataloader."""

    def setup_method(self):
        """Setup method."""
        self.configs = get_test_configs()
        self.dataloader = JsonDataloader(get_test_configs())
        self.file_path = self.configs['JSON']['annotations_path']
        self.json_parse = ('{"imageId": "000001", '
                           '"boxes": [{"boxId": 0, "rect": [0.1578125, '
                           '0.3229166666666667, 0.421875, 0.6291666666666667], "objectType": "car", '
                           '"certainty": 0.25950899720191956}, {"boxId": 1, "rect": [0.015625, '
                           '0.29791666666666666, 0.4375, 0.6333333333333333], "objectType": "truck", '
                           '"certainty": 0.2787831425666809}, {"boxId": 2, "rect": [0.0015625, '
                           '0.3541666666666667, 0.071875, 0.6125], "objectType": "car", "certainty": '
                           '0.312270849943161}, {"boxId": 3, "rect": [0.8890625, 0.4270833333333333, '
                           '1.0, 0.5729166666666666], "objectType": "car", "certainty": '
                           '0.817171037197113}, {"boxId": 4, "rect": [0.1796875, 0.325, 0.309375, '
                           '0.6875], "objectType": "person", "certainty": 0.8253413438796997}, {"boxId": '
                           '5, "rect": [0.0265625, 0.30416666666666664, 0.14375, 0.7020833333333333], '
                           '"objectType": "person", "certainty": 0.8302398920059204}]}')
        self.annotations = [('000001', 4, 0.1796875, 0.325, 0.309375, 0.6875, 0.8253413438796997, 'person', None)]

    def test_init(self):
        """Tests the init."""
        assert self.dataloader.file_path == self.configs['JSON']['annotations_path']

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        assert self.dataloader.get_annotations()[0] == self.json_parse

    def test_parse_line(self):
        """Tests parsing of file."""
        assert JsonDataloader.parse_line(self.dataloader, self.dataloader.get_annotations()[0])[4]\
               == self.annotations[0]


if __name__ == '__main__':
    pytest.main(TestJsonDataloader)
