"""Tests the draw.py functions in utils.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import random
import numpy as np
from processor.utils.draw import draw_bounding_boxes
from tests.unittests.utils.conftest import X0, X1, Y0, Y1


class TestDraw:
    """Tests the draw methods."""
    def test_draw_bounding_boxes(self, img, bbox):
        """tests the draw_bounding_boxes function.

        Args:
            img (np.ndarray): Image to draw on.
            bbox (BoundingBox): Bounding box to draw on the image.
        """
        # The color from draw_bounding_boxes is BGR red.
        red = np.array([0, 0, 255])

        # Do the draw_bounding_boxes method.
        draw_bounding_boxes(img, [bbox])

        # Assert the rectangle is correct.
        self.__assert_rectangle(img, red)

    def test_draw_boxes(self, img, bbox, func_text_seed):
        """Tests the draw_detection_boxes and draw_tracking_boxes functions.

        Args:
            img (np.ndarray): Image to draw on.
            bbox (BoundingBox): Bounding box to draw on the image.
            func_text_seed (dict[str, func]): Dictionary containing all the information for generating a color.
        """
        # Color depends on the seed.
        color = self.__get_random_color(func_text_seed["seed"])

        # Run the given function.
        func_text_seed["func"](img, [bbox])

        # Assert the rectangle is correct.
        self.__assert_rectangle(img, color)

        # Extract the text box from the image.
        sliced_img = self.__extract_text_box(img, func_text_seed["text"])

        # Assert the text box is correct.
        self.__assert_text_box(sliced_img, color)

    @staticmethod
    def __assert_rectangle(img, color):
        """Tests if the rectangle is the given color.

        Args:
            img (np.ndarray): The image to check.
            color (np.array): The color to check for.
        """
        # Test if the rectangle is red.
        x, y = X0, Y0
        while x < X1:
            assert (img[y, x] == color).all()
            x += 1
        while y < Y1:
            assert (img[y, x] == color).all()
            y += 1
        while x >= X0:
            assert (img[y, x] == color).all()
            x -= 1
        while y >= Y0:
            assert (img[y, x] == color).all()
            y -= 1

    @staticmethod
    def __assert_text_box(img, color):
        """Asserts the text box has either the black color of text or the color of the rectangle.

        Args:
            img (np.ndarray): The sliced image to check.
            color (np.array): Color to check for.
        """
        rows, columns, _ = img.shape
        # Check each pixel in the sliced image to be either the rectangle or text color.
        for i in range(rows):
            for j in range(columns):
                assert (img[i, j] == color).all() or (img[i, j] == [0, 0, 0]).all()

    @staticmethod
    def __get_random_color(seed):
        """Returns a color the same way the draw methods gets a color.

        Args:
            seed (str): Seed of the random generator.

        Returns:
            np.array: A three-element array corresponding to BGR of the color.
        """
        random.seed(seed)
        return np.array(random.sample(range(10, 255), 3))

    @staticmethod
    def __extract_text_box(img, text):
        """Extract the text box from the image.

        Args:
            img (np.ndarray): The frame to extract the text box from.
            text (str): The text that is written inside the text box.

        Returns:
            np.ndarray: a slice of the img.
        """
        return img[
               Y0 - 38:Y0,
               X0 - 1:X0 + len(text) * 15
               ]
