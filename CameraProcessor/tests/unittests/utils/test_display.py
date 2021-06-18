"""Test display.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

# For use of fixtures import is needed.
import pytest  # pylint: disable=unused-import

from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.frame_obj import FrameObj
import processor.utils.display as display


def test_display_concatinates(small_frame):
    """Tests whether the images get tiled.

    Args:
        small_frame (numpy.ndarray): Frame that gets manipulated.
    """
    height, width, _ = small_frame.shape
    frame_obj = FrameObj(small_frame, 0)

    # Tile the images.
    tiled_images = display.generate_tiled_image(frame_obj,
                                                BoundingBoxes([]),
                                                BoundingBoxes([]),
                                                BoundingBoxes([])
                                                )

    # Assert dimensions.
    tiled_height, tiled_width, _ = tiled_images.shape
    assert tiled_height == 2 * height
    assert tiled_width == 2 * width


def test_display_takes_dimensions(small_frame):
    """Assert tiling is done correctly when given dimensions.

    Args:
        small_frame (numpy.ndarray): Frame that gets manipulated.
    """
    target_dimensions = (100, 150)
    frame_obj = FrameObj(small_frame, 0)

    # Tile image given target dimensions.
    tiled_images = display.generate_tiled_image(frame_obj,
                                                BoundingBoxes([]),
                                                BoundingBoxes([]),
                                                BoundingBoxes([]),
                                                target_dimensions
                                                )

    # Asserts the dimensions.
    tiled_height, tiled_width, _ = tiled_images.shape
    assert tiled_height == target_dimensions[1] * 2
    assert tiled_width == target_dimensions[0] * 2


def test_display_automatically_downscales(large_frame):
    """When dimensions are not given but frame is too big it should downscale.

    Args:
        large_frame (numpy.ndarray): Frame that gets downsized.
    """
    height, width, _ = large_frame.shape
    frame_obj = FrameObj(large_frame, 0)

    # Generate the tiled images without specifying dimensions.
    tiled_images = display.generate_tiled_image(frame_obj,
                                                BoundingBoxes([]),
                                                BoundingBoxes([]),
                                                BoundingBoxes([])
                                                )

    # Assert new dimensions.
    tiled_height, tiled_width, _ = tiled_images.shape
    assert tiled_height <= 2 * height
    assert tiled_width <= 2 * width
