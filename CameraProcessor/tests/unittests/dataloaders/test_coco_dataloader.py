"""Tests the COCO dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.coco_dataloader import CocoDataloader
from processor.utils.config_parser import ConfigParser


class TestCocoDataloader:
    """Tests the COCO dataloader."""

    def setup_method(self):
        """Setup method."""
        self.configs = get_test_configs()
        self.dataloader = CocoDataloader(self.configs)

    def test_init(self):
        """Tests the init."""
        assert self.dataloader.file_path == self.configs['COCO']['annotations_path']
        assert self.dataloader.image_path == self.configs['COCO']['image_path']
        assert self.dataloader.coco is not None

    def test_download_coco_image(self):
        """Download a coco image from the dataset and verify it is loaded."""
        self.dataloader.download_coco_image(100)

        images

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        pass

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        pass

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        pass


if __name__ == '__main__':
    pytest.main(TestCocoDataloader)
