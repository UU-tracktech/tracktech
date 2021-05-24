"""Tests the reid utils

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import cv2
import numpy as np
from processor.utils.features import slice_bounding_box, resize_cutout
from tests.unittests.utils.conftest import X0, X1, Y0, Y1


class TestReidUtils:
    """Class to hold functions to test reid utils

    """

    def test_slice_bounding_box(self, img, bbox):
        """Tests the slice_bounding_box method

        """
        # red color to fill the bbox
        color = np.array([0, 0, 255])

        # Color the bounding box rectangle in the image
        cv2.rectangle(img,
                      (X0, Y0),
                      (X1, Y1),
                      (0, 0, 255),
                      -1)
        # Slice the image
        sliced = slice_bounding_box(bbox, img)

        # Assert the sliced image is now entirely red
        width, height, _ = sliced.shape
        for i in range(0, width):
            for j in range(0, height):
                assert (sliced[i, j] == color).all()

    def test_resize(self, img, configs):
        """Tests the resize function

        """
        size = configs['Reid'].gettuple('size')
        assert size[0], size[1] == resize_cutout(img, configs).shape
