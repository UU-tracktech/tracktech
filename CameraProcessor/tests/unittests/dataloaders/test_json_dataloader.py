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

    def test_init(self):
        """Tests the init."""
        configs = get_test_configs()
        assert self.dataloader.file_path == configs['JSON']['annotations_path']

    def test_get_annotations(self):
        """Tests getting json annotations."""
        # Only tests the start of the JSON string.
        assert self.dataloader.get_annotations()[0].startswith(
            '{"imageId": "000001", "boxes": [{'
            '"boxId": 0, "rect": [0.1578125, 0.3229166666666667, 0.421875, 0.6291666666666667], '
            '"objectType": "car", "certainty": 0.25950899720191956}, '
        )

    def test_parse_line(self):
        """Tests parsing of file."""
        # First result of the annotations against the expected result.
        assert JsonDataloader.parse_line(self.dataloader, self.dataloader.get_annotations()[0])[4]\
               == ('000001', 4, 0.1796875, 0.325, 0.309375, 0.6875, 0.8253413438796997, 'person', None)


if __name__ == '__main__':
    pytest.main(TestJsonDataloader)
