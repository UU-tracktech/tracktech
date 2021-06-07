"""Run a detection algorithm and writes the detections to a detection file.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import sys

from processor.pipeline.reidentification.reid_data import ReidData
from processor.input.image_capture import ImageCapture
from processor.utils.config_parser import ConfigParser
from processor.utils.create_runners import create_detector, create_tracker
from processor.utils.text import boxes_to_accuracy_json, boxes_to_txt

curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(f'{curr_dir}/../')
sys.path.insert(0, os.path.join(curr_dir, 'pipeline/detection/yolov5'))
sys.path.insert(0, os.path.join(curr_dir, '../detection'))


def main(configs):
    """Runs YOLOv5 detection on a video file specified in configs.ini.

    Args:
        configs (ConfigParser): Configurations to run the accuracy with.
    """
    captures = __get_captures(configs)

    for capture, dest in captures:

        print('I will write the detection objects to a txt file')
        detection_dest = dest + '.json'
        tracking_dest = dest + '.txt'
        detection_file = open(detection_dest, 'w')
        tracking_file = open(tracking_dest, 'w')

        # Instantiate the detector.
        print("Instantiating detector...")
        detector = create_detector(configs['Accuracy']['detector'], configs)
        tracker = create_tracker(configs['Accuracy']['tracker'], configs)

        # Frame counter starts at 0. Will probably work differently for streams.
        print("Starting video stream...")

        # Empty reid data.
        reid_data = ReidData()
        track_write_list = []

        while capture.opened():
            # Set the detected bounding box list to empty.
            ret, frame_obj = capture.get_next_frame()

            if not ret:
                continue

            detected_boxes = detector.detect(frame_obj)
            tracked_boxes = tracker.track(frame_obj, detected_boxes, reid_data)
            image_id = capture.image_names[capture.image_index].split('.')[0]

            # Feedback (useful for large files).
            print(image_id)

            # Convert boxes to string.
            for bounding_box in tracked_boxes:
                tracked_boxes_string = boxes_to_txt([bounding_box], frame_obj.shape, image_id)
                track_write_list.append((bounding_box.identifier, image_id, tracked_boxes_string))

            # Convert boxes to string.
            detected_boxes_string = boxes_to_accuracy_json(detected_boxes,
                                                           image_id)

            # Write boxes found by detection to.
            try:
                detection_file.write(f'{detected_boxes_string}\n')
            except RuntimeError as run_error:
                print(f'Cannot write to the file with following exception: {run_error}')

        # Sorting the list.
        track_write_list.sort(key=lambda e: e[:2])
        track_write_list = [x[2] for x in track_write_list]
        track_write_list[len(track_write_list) - 1] = track_write_list[len(track_write_list) - 1].rstrip("\n")

        print(image_id)

        try:
            tracking_file.writelines(track_write_list)
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')

        # Close files.
        detection_file.close()
        tracking_file.close()


def __get_captures(configs):
    """Gets all the captures in a folder

    Args:
        configs (ConfigParser): Configurations to run the accuracy with.

    Returns:
        captures ([(ImageCapture, det_path)]): List of captures used for detection. Datasets only use image captures.
    """
    accuracy_config = configs['Accuracy']
    config_dir = accuracy_config['source_path']
    det_path = accuracy_config['det_path']
    captures = []
    if accuracy_config['data_structure'].lower() == 'normal':
        captures.append((ImageCapture(config_dir), det_path))
        return captures

    elif accuracy_config['data_structure'].lower() == 'mot':
        for mot_test in os.listdir(accuracy_config['source_path']):
            images_path = os.path.realpath(os.path.join(config_dir, mot_test, 'img1'))
            path = os.path.realpath(os.path.join(det_path, '..', 'mot', mot_test))
            capture = ImageCapture(images_path)
            captures.append((capture, path))
        return captures
    else:
        print(1 / 0)

    return captures


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini', True)
    main(config_parser.configs)
