"""Tests the MOT datalaoder.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.mot_dataloader import MotDataloader


class TestMotDataloader:
    """Tests the MOt dataloader."""

    def setup_method(self):
        """Setup method."""
        configs = get_test_configs()
        self.dataloader = MotDataloader(configs)

    def test_parse_file(self):
        """Tests parsing of file."""
        pass

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        dimensions = self.dataloader.get_image_dimensions(1)
        assert dimensions == (640, 480)

    def test_get_image_dimensions_twice(self):
        """Tests the return from the dictionary."""
        dimensions = self.dataloader.get_image_dimensions(2)
        assert dimensions == (640, 480)

        # Get the dimensions again.
        repeated_dimensions = self.dataloader.get_image_dimensions(2)
        assert repeated_dimensions == dimensions

    def test_init(self):
        """Tests the init."""
        assert len(self.dataloader.image_dimensions) == 0

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        pass

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        pass


if __name__ == '__main__':
    pytest.main(TestMotDataloader)
