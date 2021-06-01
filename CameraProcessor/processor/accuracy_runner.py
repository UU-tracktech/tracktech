"""Run a detection algorithm and writes the detections to a detection file.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import sys

from processor.input.image_capture import ImageCapture
from processor.utils.config_parser import ConfigParser
from processor.utils.text import boxes_to_txt
from processor.utils.create_runners import create_tracker, create_detector
from processor.data_object.reid_data import ReidData

curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(f'{curr_dir}/../')
sys.path.insert(0, os.path.join(curr_dir, 'pipeline/detection/yolov5'))
sys.path.insert(0, os.path.join(curr_dir, '../detection'))


def main(configs):
    """Runs YOLOv5 detection on a video file specified in configs.ini.

    Args:
        configs (ConfigParser): Configurations to run the accuracy with.
    """
    # Initialize the accuracy config.
    accuracy_config = configs['Accuracy']

    print('I will write the detection objects to a txt file')

    # Capture the image stream.
    capture = ImageCapture(accuracy_config['source_path'])

    # Instantiate the detector.
    print("Instantiating detector...")
    detector, _ = create_detector(configs['Accuracy']['detector'], configs)
    tracker = create_tracker(configs['Accuracy']['tracker'], configs)

    # Frame counter starts at 0. Will probably work differently for streams.
    print("Starting video stream...")
    counter = 1

    # Reid data.
    reid_data = ReidData()

    # List for sorting the writed data.
    write_list = []

    # Using default values.
    shape = [10000, 10000]
    while capture.opened():
        # Set the detected bounding box list to empty.
        ret, frame_obj = capture.get_next_frame()

        if not ret:
            continue

        detected_boxes = detector.detect(frame_obj)
        tracked_boxes = tracker.track(frame_obj, detected_boxes, reid_data)

        # Convert boxes to string.
        for bounding_box in tracked_boxes.get_bounding_boxes():
            boxes_string2 = boxes_to_txt([bounding_box], frame_obj.get_shape(), counter)
            write_list.append((bounding_box.get_identifier(), counter, boxes_string2))

        shape = frame_obj.get_shape()
        counter += 1

    # Sorting the list.
    write_list.sort(key=lambda e: e[:2])
    write_list = [x[2] for x in write_list]
    write_list[len(write_list) - 1] = write_list[len(write_list) - 1].rstrip("\n")

    accuracy_dest = accuracy_config['det_path']
    accuracy_info_dest = accuracy_config['det-info_path']
    detection_file = open(accuracy_dest, 'w')
    detection_file_info = open(accuracy_info_dest, 'w')

    # Write boxes to file.
    try:
        for entry in write_list:
            detection_file.write(entry)
    except RuntimeError as run_error:
        print(f'Error encountered during writing to file: {run_error}')

    # Close files.
    detection_file.close()
    detection_file_info.write(f'{counter-1},{shape[0]},{shape[1]}')
    detection_file_info.close()


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini')
    main(config_parser.configs)
