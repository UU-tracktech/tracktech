"""Has utility functions for the reid.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import cv2


def slice_bounding_box(bbox, img):
    """Slices the bounding box out of the image given.

    Note:
        DO NOT ALTER THE RETURNED IMAGE SLICE DIRECTLY! This will alter the original image. If you absolutely
        need to do something to it, use copy() first. This is unrecommended, since copying an array is costly.

        The original image will continue to exist in memory as long as the reference made here continues
        to exist. To let Python garbage collection free the memory, you have to assign the variable to something new, or
        use `del`.

    Args:
        bbox (BoundingBox): A BoundingBox, which holds the rectangle we need
        img (np.ndarray): the numpy array representing the frame/image

    Returns:
         np.ndarray: a REFERENCE to a slice of the original image

    Examples:
        a = slice_bounding_box(bbox, img) # Assign variable a to reference the slice
        img = None # Remove the reference to the original image. IT IS STILL RETAINED IN MEMORY!!
        a = None # However, now that the slice of the image is also unreferenced, Python garbage collection will free up
                   the memory!
    """
    height, width, _ = img.shape
    return img[
           int(bbox.rectangle.y1 * height):int(bbox.rectangle.y2 * height),
           int(bbox.rectangle.x1 * width):int(bbox.rectangle.x2 * width)
           ]


def resize_cutout(cutout, configs):
    """Function that resizes the cutout to specified size in the configs.

    Args:
        cutout (np.ndarray): an np.ndarray representing the cutout you want to resize. In most cases, this is a
            reference to the original image.
        configs (configparser.SectionProxy): Re-ID configuration.

    Returns:
         np.ndarray: A resized image, which will also be a reference. Therefore, any adjustments to the original
         image reflect on this resized slice of the image too. But maybe not the other way around, since I am not sure
         if this constitutes a "shallow copy"!
    """
    # Read size from the config.
    size = configs.gettuple('size')

    # Return the cutout, which is another reference to the original image.
    return cv2.resize(cutout, size, interpolation=cv2.INTER_AREA)
