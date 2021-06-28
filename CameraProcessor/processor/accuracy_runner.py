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
from processor.utils.datawriter import get_data_writer

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

    for capture, det_writer, track_writer in captures:

        # Instantiate the detector.
        print("Instantiating detector...")
        detector = create_detector(configs['Accuracy']['detector'], configs)
        tracker = create_tracker(configs['Accuracy']['tracker'], configs)

        # Empty reid data.
        reid_data = ReidData()

        while capture.opened():
            # Set the detected bounding box list to empty.
            ret, frame_obj = capture.get_next_frame()

            if not ret:
                continue
            image_id = int(capture.image_names[capture.image_index].split('.')[0])
            detected_boxes = detector.detect(frame_obj)
            tracked_boxes = tracker.track(frame_obj, detected_boxes, reid_data)

            # Feedback (useful for large files).
            print(image_id)

            det_writer.write(detected_boxes)
            track_writer.write(tracked_boxes)

        # Close files.
        det_writer.close()
        track_writer.close()


def __get_captures(configs):
    """Gets all the captures in a folder.

    Args:
        configs (ConfigParser): Configurations to run the accuracy with.

    Returns:
        captures ([(ImageCapture, DataWriter, DataWriter)]): List of Tuples containing a capture and 2 DataWriters.
    """
    runner_config = configs['Runner']
    data_folder = runner_config['data_path']
    data_set_name = runner_config['data_set']
    det_path = runner_config['runs_path']
    runs_name = runner_config['runs_name']
    data_path_prefix = os.path.realpath(os.path.join(data_folder, data_set_name))
    det_path = os.path.realpath(os.path.join(det_path, data_set_name))
    captures = []
    if runner_config['data_structure'].lower() == 'coco':
        image_path = os.path.realpath(os.path.join(data_path_prefix, 'images'))
        det_writer = get_data_writer(configs, 'detection', det_path)
        configs['Runner']['tracking'] = 'fake'
        track_writer = get_data_writer(configs, 'tracking', det_path)
        captures.append((ImageCapture(image_path), det_writer, track_writer))
        return captures

    if runner_config['data_structure'].lower() == 'mot':
        gt_root = os.path.realpath(os.path.join(data_path_prefix, 'train'))
        det_folder, track_folder = __get_mot_folders(det_path, runs_name)
        __check_seq_maps(gt_root, data_set_name)
        for mot_test in os.listdir(gt_root):
            if mot_test == 'seqmaps':
                continue
            images_path = os.path.realpath(os.path.join(data_path_prefix, 'train', mot_test, 'img1'))
            det_path = os.path.realpath(os.path.join(det_folder, mot_test))
            track_path = os.path.realpath(os.path.join(track_folder, mot_test))
            det_writer = get_data_writer(configs, 'detection', det_path)
            track_writer = get_data_writer(configs, 'tracking', track_path)
            capture = ImageCapture(images_path)
            captures.append((capture, det_writer, track_writer))
        return captures
    raise NotImplementedError('This file format is not supported')


def __check_seq_maps(gt_root, data_set_name):
    """Check if a seq map directory exists, if not, make one automatically.

    Args:
        gt_root (string): root directory of the ground truth.
        data_set_name (string): name of the MOT dataset.
    """
    seq_map_folder = os.path.join(gt_root, 'seqmaps')
    if not os.path.exists(seq_map_folder):
        lines = ['name\n']
        for seq in os.listdir(gt_root):
            lines.append(seq + '\n')
        os.makedirs(seq_map_folder)
        file_name = data_set_name + '-train.txt'
        seq_map_file_path = os.path.realpath(os.path.join(seq_map_folder, file_name))
        seq_map_file = open(seq_map_file_path, 'w')
        seq_map_file.writelines(lines)
        seq_map_file.close()


def __get_mot_folders(path_prefix, runs_name):
    """Making folders if they do not exist.

    Args:
        path_prefix (string): Directory where the runs need to be stored.
        runs_name (string): name of the runs.

    Returns:
        det_folder (string): folder where the detection runs are stored.
        track_folder (string): folder where the tracker detections are stored.
    """
    # If it does not exist, then Initialize the directory.
    folder_name = os.path.join(path_prefix, runs_name)
    track_folder = os.path.join(folder_name, 'data')
    det_folder = os.path.join(folder_name, 'det')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        os.makedirs(track_folder)
        os.makedirs(det_folder)
    return det_folder, track_folder


if __name__ == '__main__':
    config_parser = ConfigParser('configs.ini', True)
    main(config_parser.configs)
