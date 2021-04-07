import time
import os
import sys
import configparser
import cv2
from absl import app
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import tag_constants
# pylint: disable=import-error
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
# pylint: enable=import-error
import matplotlib.pyplot as plt
from src.pipeline.detection.detection_obj import DetectionObj
from src.pipeline.tracking.tracking_obj import TrackingObj
from src.pipeline.detection.yolov4deepsort import object_tracker as ObjectTracker

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(curr_dir, '../detection'))
sys.path.insert(0, os.path.join(curr_dir, 'tracking'))


def main(_argv):
    """Runs the YOLOv4 and DeepSORT Tracker on venice.mp4

    NOTE: Any function that calls the yolov4 object_tracker or any other such detection model will
    probably have to instantiate a Tensorflow session. Without a persistent session it won't work.
    So if you're planning on writing your own testing python script, pay attention to how the
    Tensorflow models are loaded here.
    """
    # Load the config file
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read(('../configs.ini'))
    yolov4config = configs['Yolov4']

    # Initialize the tracker.
    # Tracker has to be persistent across function calls to object_tracker.py
    tracker = ObjectTracker.initialize_tracker()

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    # pylint: disable=unused-variable
    session = InteractiveSession(config=config)
    # pylint: enable=unused-variable

    # load tflite model if flag is set
    if yolov4config['framework'] == 'tflite':
        interpreter =\
            tf.lite.Interpreter(os.path.join(curr_dir, yolov4config['weights']))
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    # otherwise load standard tensorflow saved model
    else:
        saved_model_loaded = tf.saved_model.load(os.path.join(curr_dir, yolov4config['weights']),
                                                 tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    local_time = time.localtime()

    # Instantiate the Detection Object
    det_obj = DetectionObj(local_time, None, 0)
    trac_obj = TrackingObj(det_obj, None)

    # Capture the video stream
    vid = cv2.VideoCapture(os.path.join(curr_dir, yolov4config['source']))

    # Frame counter starts at 0. Will probably work differently for streams
    counter = 0
    while vid.isOpened():
        ret, frame = vid.read(0)

        if not ret:
            if counter == vid.get(cv2.CAP_PROP_FRAME_COUNT):
                print("End of file")
            else:
                raise ValueError("Feed has been interrupted")

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = counter
        det_obj.timestamp = time.localtime()

        # Run the object detector and tracker
        if yolov4config['framework'] == 'tflife':
            ObjectTracker.detect_and_track(det_obj, trac_obj, tracker, interpreter)
        else:
            ObjectTracker.detect_and_track(det_obj, trac_obj, tracker, infer)

        # Draw the frame with bounding boxes
        draw_and_show(det_obj.frame, det_obj.bounding_boxes)
        counter += 1


# This method draws every bounding boxes in given list into the given frame

# ARGUMENTS:
# frame: The frame to draw on and display
# boxes: list of bounding boxes with each bounding box being of format [x1, y1, x2, y2]


def draw_and_show(frame, boxes):
    # initialize color map
    cmap = plt.get_cmap('tab20b')
    colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

    # Draw every bounding box on top of the frame
    for i in boxes:
        color = colors[int(i.identifier) % len(colors)]
        color = [c * 255 for c in color]
        cv2.rectangle(frame, (int(i.rectangle[0]), int(i.rectangle[1])),
                      (int(i.rectangle[2]), int(i.rectangle[3])),
                      color, 2)
        cv2.rectangle(frame, (int(i.rectangle[0]), int(i.rectangle[1] - 30)),
                      (
                      int(i.rectangle[0]) + (len(i.classification) + len(str(i.identifier))) * 17,
                      int(i.rectangle[1])),
                      color, -1)
        cv2.putText(frame, i.classification + "-" + str(i.identifier),
                    (int(i.rectangle[0]), int(i.rectangle[1] - 10)),
                    0, 0.75,
                    (255, 255, 255), 2)

    # Play the video in a window called "Output Video"
    try:
        cv2.imshow("Output Video", frame)
    except Exception as err:
        # Figure out how to get Docker to use GUI
        raise Exception("Error displaying video. Are you running this in Docker perhaps?") from err

    # Waitkey command with > 0 lets frame render
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
