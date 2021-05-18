"""Tests the draw.py functions in utils

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import random
import numpy as np
from processor.utils.draw import draw_bounding_boxes
from tests.unittests.utils.conftest import X0, X1, Y0, Y1


class TestDraw:
    """Tests the draw methods

    """

    def test_draw_bounding_boxes(self, img, bbox):
        """tests the draw_bounding_boxes function

        """
        # The color from draw_bounding_boxes is BGR red
        red = np.array([0, 0, 255])

        # Do the draw_bounding_boxes method
        draw_bounding_boxes(img, [bbox])

        # Assert the rectangle is correct
        self.__assert_rectangle(img, red)

    def test_draw_boxes(self, img, bbox, func_text_seed):
        """Tests the draw_detection_boxes and draw_tracking_boxes functions. Can be extended
        with other draw functions in the fixture

        """
        # Color depends on the seed
        color = self.__get_random_color(func_text_seed["seed"])

        # Run the given function
        func_text_seed["func"](img, [bbox])

        # Assert the rectangle is correct
        self.__assert_rectangle(img, color)

        # Extract the text box from the image
        sliced_img = self.__extract_text_box(img, func_text_seed["text"])

        # Assert the text box is correct
        self.__assert_text_box(sliced_img, color)

    @staticmethod
    def __assert_rectangle(img, color):
        """Tests if the rectangle is the color

        Args:
            img (np.ndarray): the image to check
            color(np.array): the color to check for
        """
        # Test if the rectangle is red
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
        """Asserts the text box has either the black color of text or the color of the rectangle

        Args:
            img (np.ndarray): the sliced image to check
            color (np.array): the color to check for
        """
        # We check each pixel in the sliced image, to check if
        # each pixel is either the rectangle color or text color
        # Ugly testing? Yes. Coolest thing to do would be text
        # recognition but that is over-engineering
        rows, columns, _ = img.shape
        for i in range(rows):
            for j in range(columns):
                assert (img[i, j] == color).all() or (img[i, j] == [0, 0, 0]).all()

    @staticmethod
    def __get_random_color(seed):
        """Returns a color the same way the draw methods gets a color

        Returns:
            np.array: a three-element array corresponding to BGR of the color
        """
        random.seed(seed)
        return np.array(random.sample(range(10, 255), 3))

    @staticmethod
    def __extract_text_box(img, text):
        """

        Args:
            img (np.ndarray): the frame to extract the text box from
            bbox (BoundingBox): the BoundingBox whose classification/id is drawn on the image

        Returns:
            np.ndarray: a slice of the img
        """
        return img[
               Y0 - 38:Y0,
               X0 - 1:X0 + len(text) * 15
               ]
