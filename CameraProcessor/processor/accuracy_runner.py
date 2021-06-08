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
from processor.dataloaders.mot_dataloader import MOTDataloader
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.bounding_box import BoundingBox

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
    det_boxes = __get_det_boxes()
    index = 0

    for capture, dest in captures:

        print('I will write the detection objects to a txt file')
        detection_dest = dest + '.json'
        tracking_dest = dest + '.txt'
        detection_file = open(detection_dest, 'w')
        tracking_file = open(tracking_dest, 'w')

        # Instantiate the detector.
        print("Instantiating detector...")
        # detector = create_detector(configs['Accuracy']['detector'], configs)
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
            image_id = int(capture.image_names[capture.image_index].split('.')[0])
            detected_boxes = det_boxes[index][image_id-1] # detector.detect(frame_obj)
            tracked_boxes = tracker.track(frame_obj, detected_boxes, reid_data)


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

        try:
            tracking_file.writelines(track_write_list)
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')

        # Close files.
        detection_file.close()
        tracking_file.close()
        index += 1


def __get_det_boxes():
    all_dets = []
    configs_01 = ConfigParser('configs.ini', True).configs
    configs_01['Accuracy']['det_path'] = os.path.realpath('./../../IdealDets/MOT20-01.txt')
    configs_01['Accuracy']['image_path'] = os.path.realpath('./../../MOT20/train/MOT20-01/img1')
    configs_01['Accuracy']['nr_frames'] = '429'
    data_loader_01 = MOTDataloader(configs_01, 'det_path')
    boxes_01 = data_loader_01.parse_file()
    dets_01 = []
    for box in boxes_01:
        dets_01.append(box)
    all_dets.append(__sort_boxes(dets_01, 429))

    configs_02 = ConfigParser('configs.ini', True).configs
    configs_02['Accuracy']['det_path'] = os.path.realpath('./../../IdealDets/MOT20-02.txt')
    configs_02['Accuracy']['image_path'] = os.path.realpath('./../../MOT20/train/MOT20-02/img1')
    configs_02['Accuracy']['nr_frames'] = '2782'
    data_loader_02 = MOTDataloader(configs_02, 'det_path')
    boxes_02 = data_loader_02.parse_file()
    dets_02 = []
    for box in boxes_02:
        dets_02.append(box)
    all_dets.append(__sort_boxes(dets_02, 2782))

    configs_03 = ConfigParser('configs.ini', True).configs
    configs_03['Accuracy']['det_path'] = os.path.realpath('./../../IdealDets/MOT20-03.txt')
    configs_03['Accuracy']['image_path'] = os.path.realpath('./../../MOT20/train/MOT20-03/img1')
    configs_03['Accuracy']['nr_frames'] = '2405'
    data_loader_03 = MOTDataloader(configs_03, 'det_path')
    boxes_03 = data_loader_03.parse_file()
    dets_03 = []
    for box in boxes_03:
        dets_03.append(box)
    all_dets.append(__sort_boxes(dets_03, 2405))

    configs_05 = ConfigParser('configs.ini', True).configs
    configs_05['Accuracy']['det_path'] = os.path.realpath('./../../IdealDets/MOT20-05.txt')
    configs_05['Accuracy']['image_path'] = os.path.realpath('./../../MOT20/train/MOT20-05/img1')
    configs_05['Accuracy']['nr_frames'] = '3315'
    data_loader_05 = MOTDataloader(configs_05, 'det_path')
    boxes_05 = data_loader_05.parse_file()
    dets_05 = []
    for box in boxes_05:
        dets_05.append(box)
    all_dets.append(__sort_boxes(dets_05, 3315))
    return all_dets


def __sort_boxes(list_bbox, nr_frames):
    sorted_boxes = []
    # Creating data structure.
    for i in range(nr_frames):
        sorted_boxes.append([])
    for bboxes in list_bbox:
        image_id = bboxes.image_id
        for bbox in bboxes.bounding_boxes:
            sorted_boxes[image_id-1].append(bbox)
    return sorted_boxes


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
