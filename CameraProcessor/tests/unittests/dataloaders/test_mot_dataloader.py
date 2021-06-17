"""Tests the MOT datalaoder.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest


from tests.conftest import get_test_configs
from processor.dataloaders.mot_dataloader import MotDataloader


# pylint: disable=attribute-defined-outside-init
class TestMotDataloader:
    """Tests the MOt dataloader."""

    def setup_method(self):
        """Setup method."""
        self.configs = get_test_configs()
        self.dataloader = MotDataloader(self.configs)
        self.file_path = self.dataloader.file_path
        self.image_path = self.dataloader.image_path
        self.image_dimensions = self.dataloader.image_dimensions
        self.skipped_lines = self.dataloader.skipped_lines
        self.delimiter = self.dataloader.delimiter

    def test_init(self):
        """Tests the init."""
        configs = get_test_configs()
        assert len(self.dataloader.image_dimensions) == 0

        assert self.file_path == configs['MOT']['annotations_path']
        assert self.image_path == configs['MOT']['image_path']
        assert self.image_dimensions == {}
        assert self.skipped_lines == []
        assert self.delimiter == ' '

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        assert self.dataloader.get_annotations()[0] == '1,1,17,150,77,191,1,1,1'

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

    def test_parse_line(self):
        """Tests the parsing of line."""
        parsed_line = [(1, 1, 0.025, 0.3104166666666667, 0.1453125, 0.7083333333333334, 1, '', None)]
        assert self.dataloader.parse_line(self.dataloader.get_annotations()[0]) == parsed_line


if __name__ == '__main__':
    pytest.main(TestMotDataloader)
