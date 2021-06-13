"""Tests the dataloader interface.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.i_dataloader import IDataloader


class TestIDataloader:
    """Tests the dataloader interface.

    Attributes:
        dataloader (IDataloader): Dataloader interface to test.
    """

    def setup_method(self):
        """Setup method."""
        configs = get_test_configs()
        self.dataloader = IDataloader(configs, 'det_path')

    def test_parse_file(self):
        """Tests parsing of file."""
        assert pytest.raises(NotImplementedError, self.dataloader.parse_file)

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        image_path = os.path.join(self.dataloader.image_path, '000001.jpg')
        dimensions = self.dataloader.get_image_dimensions(1, image_path)
        assert dimensions == (640, 480)

    def test_get_image_dimensions_twice(self):
        """Tests the return from the dictionary."""
        image_path = os.path.join(self.dataloader.image_path, '000002.jpg')
        dimensions = self.dataloader.get_image_dimensions(2, image_path)
        assert dimensions == (640, 480)

        # Get the dimensions again.
        repeated_dimensions = self.dataloader.get_image_dimensions(2, image_path)
        assert repeated_dimensions == dimensions

    def test_init(self):
        """Tests the init."""
        configs = get_test_configs()
        accuracy_config = configs['Accuracy']

        # Check whether properties are set correctly.
        assert self.dataloader.file_path == accuracy_config['det_path']
        assert self.dataloader.image_path == accuracy_config['image_path']
        assert self.dataloader.categories == accuracy_config['categories']
        assert self.dataloader.filter_config == configs['Filter']
        assert len(self.dataloader.image_dimensions) == 0
        assert self.dataloader.nr_frames == int(accuracy_config['nr_frames'])

    def test_invalid_init(self):
        """Negative number of frames should raise an exception."""
        configs = get_test_configs()
        configs['Accuracy']['nr_frames'] = '-1'
        assert pytest.raises(AttributeError, IDataloader, configs, 'det_path')
