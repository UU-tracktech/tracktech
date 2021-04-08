import os
import logging
from typing import List
import cv2
from processor.input.icapture import ICapture


class ImageCapture(ICapture):
    def __init__(self, images_dir: str):
        """Gets all the paths to images inside the folder and stores them in order

        Args:
            images_dir: Path to the directory that contains the images
        """
        logging.info(f'Using images from folder {images_dir}')
        # Gets the number of images from the folder
        self.images_paths = sorted([os.path.join(images_dir, image_name)
                                    for image_name in os.listdir(images_dir)])
        self.nr_images = len(self.images_paths)

        # Start index is -1 because we want to know the index of current after it has been incremented
        self.image_index = -1
        logging.info(f'Found {self.nr_images} images inside the folder')

    def opened(self) -> bool:
        """Capture is still opened when more images are available

        Returns:
            Boolean whether there are more images to iterate
        """
        return self.image_index + 1 < self.nr_images

    def close(self) -> None:
        """Close the capture by setting the index higher than the number of images
        """
        self.image_index = self.nr_images + 1

    # Gets the next frame from the stream
    def get_next_frame(self) -> (bool, List[List[int]]):
        """Gets the next frame from the list of images

        Returns:
            Boolean whether a next image was found
            If a frame was found gives a frame back too
        """
        self.image_index += 1
        image_path = self.images_paths[self.image_index]

        # Skips when it is not a file but a directory
        if not os.path.isfile(image_path):
            logging.warning(f'File {image_path} is not a file!')
            return False, None, None

        # Reads the image file and returns it
        frame = cv2.imread(image_path)
        return True, frame, None
