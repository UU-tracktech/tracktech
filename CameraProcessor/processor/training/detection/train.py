""" File that runs training using a custom dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

# Determine training set
# Determine test set
# Verification sets

# Run test set in epochs

# Determine accuracy of a bounding box estimate
import os
import logging
import sys
import cv2

import processor.utils.draw as draw
from processor.utils.config_parser import ConfigParser
from processor.input.image_capture import ImageCapture
from processor.training.pre_annotations import PreAnnotations
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle


def main():
    """Main training function.

    Only displays the ground truth that is present in the gt.txt file.
    """
    root_dir = os.path.abspath(__file__ + '/../../../../')
    logging.basicConfig(filename=os.path.join(root_dir, 'app.log'), filemode='w',
                        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    configs_parser = ConfigParser('configs.ini')
    configs = configs_parser.configs

    images_dir = configs['Accuracy']['source_path']
    bounding_boxes_path = configs['Accuracy']['gt_path']

    capture = ImageCapture(images_dir)
    pre_annotations = PreAnnotations(bounding_boxes_path, capture.nr_images)
    pre_annotations.parse_file()
    all_frame_bounding_boxes = pre_annotations.boxes

    logging.info('start training')

    frame_nr = 0

    # As long as there is more footage
    while capture.opened():
        ret, frame_obj = capture.get_next_frame()

        # Frame not found
        if not ret:
            logging.warning('Frame inside training not found')
            continue

        width, height = frame_obj.get_shape()

        bounding_boxes = scale_boxes(all_frame_bounding_boxes[frame_nr], width, height)

        # Visualise rectangles of ground truth and show it
        draw.draw_bounding_boxes(frame_obj.get_frame(), bounding_boxes)

        cv2.imshow('Frame', frame_obj.get_frame())

        # Close loop when q is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        frame_nr += 1

    logging.info('training stopping')
    # When everything is done release the capture
    capture.close()


def scale_boxes(raw_bounding_boxes, width, height):
    """Scales boundingBoxes before drawing.

    Args:
        raw_bounding_boxes ([BoundingBox]): list of bounding boxes.
        width (float): width dimension of bounding boxes.
        height (float): height dimension of bounding boxes.

    Returns:
        [BoundingBox]: normalized bounding boxes.
    """
    bounding_boxes = []

    identifier = 0
    for raw_bounding_box in raw_bounding_boxes:
        # Scale rectangle
        rectangle = Rectangle(
            raw_bounding_box.get_rectangle().get_x1() / width,
            raw_bounding_box.get_rectangle().get_y1() / height,
            raw_bounding_box.get_rectangle().get_x2() / width,
            raw_bounding_box.get_rectangle().get_y2() / height
        )
        # Create bounding box
        bounding_boxes.append(
            BoundingBox(
                raw_bounding_box.get_identifier(),
                rectangle,
                raw_bounding_box.get_classification(),
                raw_bounding_box.get_certainty()
            )
        )

        identifier += 1

    return bounding_boxes


if __name__ == '__main__':
    main()
