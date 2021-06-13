"""Tests the COCO dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.coco_dataloader import CocoDataloader
from processor.utils.config_parser import ConfigParser


class TestCocoDataloader:
    """Tests the COCO dataloader."""

    def setup_method(self):
        """Setup method."""
        configs = get_test_configs()
        pass

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        pass

    def test_init(self):
        """Tests the init."""
        pass

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        pass

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        pass


if __name__ == '__main__':
    pytest.main(TestCocoDataloader)
