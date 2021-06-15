"""Tests the JSON dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.json_dataloader import JsonDataloader


class TestJsonDataloader:
    """Tests the JSON dataloader."""

    def setup_method(self):
        """Setup method."""
        self.configs = get_test_configs()
        self.dataloader = JsonDataloader(get_test_configs())
        self.file_path = self.configs['JSON']['annotations_path']

    def test_init(self):
        """Tests the init."""
        assert self.dataloader.file_path == self.configs['JSON']['annotations_path']

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        assert self.dataloader.get_annotations()[0] == '1,1,101,155,169,146,1,1,0.26'

    def test_parse_file(self):
        """Tests parsing of file."""
        pass

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        pass

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        pass


if __name__ == '__main__':
    pytest.main(TestJsonDataloader)
