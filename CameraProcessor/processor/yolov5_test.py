""" Testing file to display yolov5 functionality with our proprietary pipeline.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import os
import sys
import configparser
from absl import app

from processor.input.image_capture import ImageCapture
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.utils.text import boxes_to_txt

curr_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(f'{curr_dir}/../')
sys.path.insert(0, os.path.join(curr_dir, 'pipeline/detection/yolov5'))
sys.path.insert(0, os.path.join(curr_dir, '../detection'))


def main(_argv):
    """Runs YOLOv5 detection on a video file specified in configs.ini."""
    # Load the config file, take the relevant Yolov5 section
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read('../configs.ini')
    trueconfig = configs['Yolov5']
    filterconfig = configs['Filter']
    accuracy_config = configs['Accuracy']

    # Opening files where the information is stored that is used to determine the accuracy
    accuracy_dest = os.path.join('..', accuracy_config['det-path'])
    accuracy_info_dest = os.path.join('..', accuracy_config['det-info-path'])
    detection_file = open(accuracy_dest, 'a')
    detection_file_info = open(accuracy_info_dest, 'w')

    detection_file.truncate(0)
    print('I will write the detection objects to a txt file')

    # Capture the video stream
    vidstream = ImageCapture(os.path.join(curr_dir, '..', accuracy_config['source']))

    # Instantiate the detector
    print("Instantiating detector...")
    detector = Yolov5Detector(trueconfig, filterconfig)

    # Frame counter starts at 0. Will probably work differently for streams
    print("Starting video stream...")
    counter = 0
    while vidstream.opened():
        # Set the detected bounding box list to empty
        ret, frame_obj = vidstream.get_next_frame()

        if not ret:
            continue
            # Closing the detection files when the end of the stream is reached
            # if counter == vidstream.get_capture_length():
            #     print("End of file")
            #     detection_file.close()
            #     detection_file_info.close()
            # else:
            #     raise ValueError("Feed has been interrupted")
            # return

        bounding_boxes = detector.detect(frame_obj)

        # Convert boxes to string
        boxes_string = boxes_to_txt(bounding_boxes.get_bounding_boxes(), frame_obj.get_shape(), counter)

        # Write boxes found by detection to
        try:
            detection_file.write(boxes_string)
        except RuntimeError as run_error:
            print(f'Cannot write to the file with following exception: {run_error}')

        # Overwrite the file info with the new detection object
        detection_file_info.write(f'{counter},{frame_obj.get_shape()[0]},{frame_obj.get_shape()[1]}')

        counter += 1

    # Close files
    detection_file.close()
    detection_file_info.close()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
