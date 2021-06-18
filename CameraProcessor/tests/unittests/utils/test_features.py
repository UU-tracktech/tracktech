"""Tests the utils.features.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import cv2
import numpy as np

from processor.utils.features import slice_bounding_box, resize_cutout


class TestFeatures:
    """Class to hold functions to test reid utils."""
    def test_slice_bounding_box(self, img, bbox):
        """Tests the slice_bounding_box method.

        Args:
            img (np.ndarray): Image in array form.
            bbox (BoundingBox): Bounding box that gets sliced.
        """
        # Red color to fill the bbox.
        color = np.array([0, 0, 255])

        height, width, _ = img.shape

        # Color the bounding box rectangle in the image.
        cv2.rectangle(img,
                      (int(bbox.rectangle.x1 * width), int(bbox.rectangle.y1 * height)),
                      (int(bbox.rectangle.x2 * width), int(bbox.rectangle.y2 * height)),
                      (0, 0, 255),
                      -1)
        # Slice the image.
        sliced = slice_bounding_box(bbox, img)

        # Assert the sliced image is now entirely red.
        width, height, _ = sliced.shape
        for i in range(0, width):
            for j in range(0, height):
                assert (sliced[i, j] == color).all()

    def test_resize(self, img, configs):
        """Tests the resize function.

        Args:
            img (np.ndarray): Image in array form.
            configs (ConfigParser): Configparser used to determine the cutout size.
        """
        size = configs['TorchReid'].gettuple('size')
        # Assert size is correct.
        assert size[0], size[1] == resize_cutout(img, configs).shape
