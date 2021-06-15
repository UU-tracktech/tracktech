"""Tests the COCO dataloader.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import pytest

from tests.conftest import get_test_configs
from processor.dataloaders.coco_dataloader import CocoDataloader


# pylint: disable=attribute-defined-outside-init
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

        # Expected image path.
        image_name = self.dataloader.coco.loadImgs([463730])[0]['file_name']
        expected_image_path = os.path.join(self.dataloader.image_path, image_name)

        if os.path.exists(expected_image_path):
            os.remove(expected_image_path)

        # Assert that image exists AFTER download.
        self.dataloader.download_coco_image(463730)
        assert os.path.exists(expected_image_path)

    def test_download_coco_images(self):
        """Download several coco images from the dataset and verify it is downloaded."""
        # The folder name.
        image_dir = self.dataloader.image_path
        nr_images = 5

        # Assert that image exists AFTER download.
        nr_of_existing_files = len(os.listdir(image_dir))
        self.dataloader.download_coco_images(nr_images)
        assert len(os.listdir(image_dir)) == nr_of_existing_files + nr_images

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        image_json = self.dataloader.coco.loadImgs([463730])[0]
        expected_width, expected_height = int(image_json['width']), int(image_json['height'])

        actual_width, actual_height = self.dataloader.get_image_dimensions(463730)
        assert expected_width == actual_width
        assert expected_height == actual_height

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        image_json = self.dataloader.coco.loadImgs([463730])[0]
        boxes = self.dataloader.parse_boxes([image_json])
        print(boxes)

    def test_parse_line(self):
        """Tests the parse_line function."""
        assert True

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        annotations = self.dataloader.get_annotations()
        print(annotations)
        assert True


if __name__ == '__main__':
    pytest.main(TestCocoDataloader)
