""" Run a detection algorithm and writes the detections to a detection file

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import sys

from processor.input.image_capture import ImageCapture
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.utils.config_parser import ConfigParser
from processor.utils.text import boxes_to_txt

curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(f'{curr_dir}/../')
sys.path.insert(0, os.path.join(curr_dir, 'pipeline/detection/yolov5'))
sys.path.insert(0, os.path.join(curr_dir, '../detection'))


def main(configs):
    """Runs YOLOv5 detection on a video file specified in configs.ini."""
    # Load the config file, take the relevant Yolov5 section
    yolov5_config = configs['Yolov5']
    accuracy_config = configs['Accuracy']

    # Opening files where the information is stored that is used to determine the accuracy
    accuracy_dest = accuracy_config['det_path']
    detection_file = open(accuracy_dest, 'w')

    print('I will write the detection objects to a txt file')

    # Capture the image stream
    capture = ImageCapture(accuracy_config['source_path'])

    # Instantiate the detector
    print("Instantiating detector...")
    yolov5_config['device'] = "cpu"
    detector = Yolov5Detector(yolov5_config, configs['Filter'])

    # Frame counter starts at 0. Will probably work differently for streams
    print("Starting video stream...")

    while capture.opened():
        # Set the detected bounding box list to empty
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        bounding_boxes = detector.detect(frame_obj)
        image_id = capture.image_names[capture.image_index].split('.')[0]

        # Convert boxes to string
        boxes_string = boxes_to_txt(bounding_boxes.get_bounding_boxes(),
                                    image_id)

        # Write boxes found by detection to
        try:
            detection_file.write(boxes_string)
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')

        # Save the shape so it can be saved in the detection-info file
        shape = frame_obj.get_shape()

    # Close files
    detection_file.close()


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini')
    main(config_parser.configs)
