"""Has utility functions for the reid

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import numpy as np
from processor.data_object.bounding_box import BoundingBox


def slice_bounding_box(bbox, img):
    """Slices the bounding box out of the image given
    Args:
        bbox (BoundingBox): A boundingbox which holds the rectangle we need
        img (np.ndarray): the numpy array representing the frame/image

    Returns:
         np.ndarray: a REFERENCE to a lisce of the original image

    IMPORTANT: DO NOT ALTER THE RETURNED IMAGE SLICE DIRECTLY! This will alter the original image. If you absolutely
    need to do something to it, use copy() first. This is unrecommended, since copying an array is costly.
    """
    width, height, _ = img.shape
    return img[
           int(bbox.get_rectangle().get_y1() * height):int(bbox.get_rectangle().get_y2() * height),
           int(bbox.get_rectangle().get_x1() * width):int(bbox.get_rectangle().get_x2() * width)
           ]
