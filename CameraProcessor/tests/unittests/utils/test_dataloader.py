"""File for testing the function get_dataloader in processor.utils.dataloader.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from tests.conftest import get_test_configs
from processor.utils.dataloader import get_dataloader
from processor.dataloaders.coco_dataloader import CocoDataloader
from processor.dataloaders.json_dataloader import JsonDataloader
from processor.dataloaders.mot_dataloader import MotDataloader


# pylint: disable=attribute-defined-outside-init
class TestDataloader:
    """Class for testing the functions contained in processor.utils.dataloader.py."""
    def setup_method(self):
        """Setup method for getting the configs."""
        self.configs = get_test_configs()

    def test_mot_loader(self):
        """Method for testing if a MOT dataloader is returned."""
        data_loader = get_dataloader(self.configs, 'MOT')
        assert isinstance(data_loader, MotDataloader)

    def test_coco_loader(self):
        """Method for testing if a COCO dataloader is returned."""
        data_loader = get_dataloader(self.configs, 'COCO')
        assert isinstance(data_loader, CocoDataloader)

    def test_json_loader(self):
        """Method for testing if a JSON dataloader is returned."""
        data_loader = get_dataloader(self.configs, 'JSON')
        assert isinstance(data_loader, JsonDataloader)

    def test_invalid_loader(self):
        """Method for testing if the correct error is thrown if there is no valid dataloader."""
        with pytest.raises(ValueError):
            get_dataloader(self.configs, 'Invalid Dataloader')
