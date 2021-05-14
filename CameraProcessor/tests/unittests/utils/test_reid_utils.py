"""Tests the reid utils

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import pytest
import cv2
import time
import numpy as np
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle
from processor.utils.reid_utils import slice_bounding_box


class TestReidUtils:
    """Class to hold functions to test reid utils

    """

    def test_slice_bounding_box(self):
        """Tests the slice_bounding_box method

        TODO refactor this so that it uses the utils.utils from branch SPC-503 branch # pylint: disable=fixme

        """
        # Empty white image
        image = np.zeros((200, 200, 3), np.uint8)
        image.fill(255)

        # A bounding box for testing
        bbox = BoundingBox(1, Rectangle(round(float(60 / 200), 1),
                                        round(float(120 / 200), 1),
                                        round(float(120 / 200), 1),
                                        round(float(180 / 200), 1)),
                           "Bob", 0.50)
        # red color to fill the bbox
        color = np.array([0, 0, 255])

        # Color the bounding box rectangle in the image
        cv2.rectangle(image,
                      (60, 120),
                      (120, 180),
                      (0, 0, 255),
                      -1)
        # Slice the image
        sliced = slice_bounding_box(bbox, image)

        # Assert the sliced image is now entirely red
        width, height, _ = sliced.shape
        for i in range(0, width):
            for j in range(0, height):
                assert (sliced[i, j] == color).all()
