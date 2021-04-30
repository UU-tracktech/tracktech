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
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.pipeline.detection.yolov5_runner import Yolov5Detector

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

    local_time = time.localtime()

    # Instantiate the Detection Object
    det_obj = DetectionObj(local_time, None, 0)

    # Opening files where the information is stored that is used to determine the accuracy
    accuracy_dest = os.path.join('..', accuracy_config['det-path'])
    accuracy_info_dest = os.path.join('..', accuracy_config['det-info-path'])
    detection_file = open(accuracy_dest, 'a')
    detection_file_info = open(accuracy_info_dest, 'w')

    detection_file.truncate(0)
    print('I will write the detection objects to a txt file')

    # Capture the video stream
    vidstream = ImageCapture(os.path.join(curr_dir, '..', trueconfig['source']))

    # Instantiate the detector
    print("Instantiating detector...")
    detector = Yolov5Detector(trueconfig, filterconfig)

    # Frame counter starts at 0. Will probably work differently for streams
    print("Starting video stream...")
    counter = 0
    while vidstream.opened():
        # Set the detected bounding box list to empty
        det_obj.bounding_box = []
        ret, frame, _ = vidstream.get_next_frame()

        if not ret:
            # Closing the detection files when the end of the stream is reached
            if counter == vidstream.get_capture_length():
                print("End of file")
                detection_file.close()
                detection_file_info.close()
            else:
                raise ValueError("Feed has been interrupted")
            return

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = counter
        det_obj.timestamp = time.localtime()

        detector.detect(det_obj)

        counter += 1

    # Close files
    detection_file.close()
    detection_file_info.close()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
