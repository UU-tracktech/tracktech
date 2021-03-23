import cv2
import os
import logging
from input.custom_capture import ICapture


class ImageCapture(ICapture):
    # Default init is public HLS stream
    def __init__(self, images_dir):
        logging.info(f'Using images from folder {images_dir}')
        self.images_paths = sorted([os.path.join(images_dir, image_name) for image_name in os.listdir(images_dir)])
        self.nr_images = len(self.images_paths)
        # Starts at -1 so after getting the image it keeps the index
        self.image_index = -1
        logging.info(f'Found {self.nr_images} images inside the folder')

    # Sees whether stream has stopped
    def stopped(self):
        return self.image_index + 1 >= self.nr_images

    # When everything is done release the capture
    def close(self):
        return

    # Gets the next frame from the stream
    def get_next_frame(self):
        self.image_index += 1
        image_path = self.images_paths[self.image_index]

        if not os.path.isfile(image_path):
            logging.warning(f'File {image_path} is not a file!')
            return False, None

        frame = cv2.imread(image_path)
        return True, frame
