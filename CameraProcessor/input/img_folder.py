import cv2
import os
import logging
from custom_capture import ICapture


class IMGCapture(ICapture):
    # Default init is public HLS stream
    def __init__(self, images_dir):
        logging.info(f'Using images from folder {images_dir}')
        self.images_paths = sorted([os.path.join(images_dir, image_name) for image_name in os.listdir(images_dir)])
        self.image_index = 0
        logging.info(f'Found {len(self.images_paths)} images inside the folder')

    # Sees whether stream has stopped
    def stopped(self):
        return self.image_index < len(self.images_paths)

    # When everything is done release the capture
    def close(self):
        return

    # Gets the next frame from the stream
    def get_next_frame(self):
        image_path = self.images_paths[self.image_index]
        self.image_index += 1

        if not os.path.isfile(image_path):
            logging.warning(f'File {image_path} is not a file!')

        frame = cv2.imread(image_path)
        return frame


working_dir = os.path.dirname(os.path.realpath(__file__))
# folder_path = os.path.join(working_dir.parent.parent, "data\\annotated\\test")
folder_path = "C:\\Users\\Gerar\\OneDrive - Universiteit Utrecht\\Documents\\University\\3.3 Bachelorproject\\TrackTech\\CameraProcessor\\data\\annotated"


    if os.path.isfile(item_path):
        continue

    frame_nr = 0
    images_dir = os.path.join(item_path, "img1")

    bounding_boxes_path = os.path.join(item_path, "gt")
    nr_images = len(os.listdir(images_dir))
    bounding_boxes = Annotations(bounding_boxes_path, nr_images).boxes

    for image_name in sorted(os.listdir(images_dir)):

