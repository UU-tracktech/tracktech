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

        #A specific image id to run tests over.
        self.coco_image_id = 463730

    def test_init(self):
        """Tests the init."""
        assert self.dataloader.file_path == self.configs['COCO']['annotations_path']
        assert self.dataloader.image_path == self.configs['COCO']['image_path']
        assert self.dataloader.coco is not None

    def test_download_coco_image(self):
        """Download a coco image from the dataset and verify it is loaded."""

        # Expected image path with fixed COCO image.
        image_name = self.dataloader.coco.loadImgs([self.coco_image_id])[0]['file_name']
        expected_image_path = os.path.join(self.dataloader.image_path, image_name)

        if os.path.exists(expected_image_path):
            os.remove(expected_image_path)

        # Assert that fixed image exists AFTER download.
        self.dataloader.download_coco_image(self.coco_image_id)
        assert os.path.exists(expected_image_path)

    def test_download_coco_images(self):
        """Download several coco images from the dataset and verify it is downloaded.

        Also contains logic to get the image names before actually downloading them.
        Then the test is able to run repeatedly without failing because the files already exist.
        """
        # Number of images to download.
        nr_images = 5

        # Specify a list of category names of interest.
        cat_ids = self.dataloader.coco.getCatIds(catNms=['person'])

        # Get the corresponding image ids and images using loadImgs.
        img_ids = self.dataloader.coco.getImgIds(catIds=cat_ids)[:nr_images]
        image_paths = [os.path.join(self.dataloader.image_path, image['file_name'])
                       for image in self.dataloader.coco.loadImgs(img_ids)]

        # Remove the images if they already exist.
        for image_path in image_paths:
            if os.path.exists(image_path):
                os.remove(image_path)

        # Assert that images exist AFTER download.
        nr_of_existing_files = len(os.listdir(self.dataloader.image_path))
        self.dataloader.download_coco_images(nr_images)
        assert len(os.listdir(self.dataloader.image_path)) == nr_of_existing_files + nr_images

    def test_get_image_dimensions(self):
        """Tests the image dimensions."""
        width, height = self.dataloader.get_image_dimensions(self.coco_image_id)

        # Compares the width and height with the expected values.
        assert width == 640
        assert height == 427

    def test_parse_boxes(self):
        """Tests the parsing of boxes."""
        annotations = self.dataloader.get_annotations()
        boxes = self.dataloader.parse_boxes(annotations)

        # Correct number of bounding boxes are created.
        assert len(boxes) == self.dataloader.nr_frames

    def test_parse_line(self):
        """Tests the parse_line function."""
        # Gets the first line of the annotations.
        annotations = self.dataloader.get_annotations()
        line = self.dataloader.parse_line(annotations[0])

        # First line of the dataloader should contain the following information.
        assert line ==\
               [(458755, 186574, 0.10785937500000001, 0.07864583333333333, 0.9016875000000001, 0.9865208333333333,
                 1, 'person', None)]

    def test_get_annotations(self):
        """Tests the get annotations functionality."""
        annotations = self.dataloader.get_annotations()

        # Assert some properties.
        assert len(annotations) > 0
        assert len(annotations[0]['bbox']) == 4
        assert annotations[0]['image_id'] > 0
        assert annotations[0].__contains__('id')
        assert annotations[0].__contains__('category_id')


if __name__ == '__main__':
    pytest.main(TestCocoDataloader)
