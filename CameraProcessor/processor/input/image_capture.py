"""Contains the ImageCapture class that reads a folder.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import time
import logging
import cv2

from processor.input.icapture import ICapture
from processor.data_object.frame_obj import FrameObj


class ImageCapture(ICapture):
    """Reads all images from a folder one by one.

    Attributes:
        images_paths (List[str]): List of paths of images in folder.
        nr_images (int): Number of images contained in folder.
        image_index (int): Index of current image frame.
    """
    def __init__(self, images_dir):
        """Gets all the paths to images inside the folder and stores them in order.

        Args:
            images_dir (str): Path to the directory that contains the images.
        """
        logging.info(f'Using images from folder {images_dir}')
        # Gets the number of images from the folder.
        self.images_paths = sorted([os.path.join(images_dir, image_name)
                                    for image_name in os.listdir(images_dir)])
        self.image_names = sorted(os.listdir(images_dir))
        self.nr_images = len(self.images_paths)

        # Start index is -1 because we want to know the index of current after it has been incremented.
        self.image_index = -1
        logging.info(f'Found {self.nr_images} images inside the folder')

    def opened(self):
        """Capture is still opened when more images are available.

        Returns:
            bool: Whether there are more images to iterate.
        """
        return self.image_index + 1 < self.nr_images

    def close(self):
        """Close the capture by setting the index higher than the number of images."""
        self.image_index = self.nr_images + 1

    def get_next_frame(self):
        """Gets the next frame from the list of images.

        Returns:
            bool, FrameObj: Boolean whether a next image was found.
                            FrameObject containing frame and missing timestamp.
        """
        # Returns False if we are at the end of the directory.
        if not self.opened():
            return False, None

        self.image_index += 1
        # Get path of next frame.
        image_path = self.images_paths[self.image_index]

        # Reads the image file and returns it.
        frame = cv2.imread(image_path)
        return True, FrameObj(frame, time.time())
