import os
import logging
import cv2
from src.input.icapture import ICapture


class ImageCapture(ICapture):
    # Default init is public HLS stream
    def __init__(self, images_dir):
        logging.info("Using images from folder %s", images_dir)
        self.images_paths = sorted([os.path.join(images_dir, image_name)
                                    for image_name in os.listdir(images_dir)])
        self.nr_images = len(self.images_paths)
        # Starts at -1 so after getting the image it keeps the index
        self.image_index = -1
        logging.info("Found %s images inside the folder", self.nr_images)

    # Sees whether stream has stopped
    def opened(self):
        return self.image_index + 1 < self.nr_images

    # When everything is done release the capture
    def close(self):
        self.image_index = self.nr_images + 1

    # Gets the next frame from the stream
    def get_next_frame(self):
        self.image_index += 1
        image_path = self.images_paths[self.image_index]

        if not os.path.isfile(image_path):
            logging.warning("File %s is not a file!", image_path)
            return False, None, None

        frame = cv2.imread(image_path)
        return True, frame, None
