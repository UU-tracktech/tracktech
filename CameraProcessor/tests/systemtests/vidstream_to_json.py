import time
import os
import sys
import configparser
import cv2
import json
from absl import app
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.pipeline.detection.bounding_box import BoundingBox
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.input.video_capture import VideoCapture
from processor.input.hls_capture import HlsCapture

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(curr_dir, '../../processor/pipeline/detection/yolov5')))


def main(_argv):
    """Runs YOLOv5 detection on a videofile specified in line 33
    and saves the JSON objecs to testdata/output.json
    """
    # Load the config file, take the relevant Yolov5 section
    configs = configparser.ConfigParser(allow_no_value=True)
    configs.read(('../../configs.ini'))
    trueconfig = configs['Yolov5']
    filterconfig = configs['Filter']

    local_time = time.localtime()

    # Instantiate the Detection Object
    det_obj = DetectionObj(local_time, None, 0)

    # Capture the video stream
    vidstream = VideoCapture(os.path.abspath(os.path.join(curr_dir, "../../data/videos/test.mp4")))

    # Instantiate the detector
    print("Instantiating detector...")
    detector = Yolov5Detector(trueconfig, filterconfig)

    # Open Json file, go to 0th line to overwrite
    outfile = open("testdata/output.json", "w")
    outfile.seek(0)
    outfile.write("[")

    # Frame counter starts at 0. Will probably work differently for streams
    print("Starting video stream...")
    counter = 0
    while vidstream.opened():
        # Set the detected bounding box list to empty
        det_obj.bounding_box = []
        ret, frame, _ = vidstream.get_next_frame()

        if not ret:
            if counter == vidstream.get_capture_length():
                print("End of file")
            else:
                raise ValueError("Feed has been interrupted")
            break

        # update frame, frame number, and time
        det_obj.frame = frame
        det_obj.frame_nr = counter
        det_obj.timestamp = time.localtime()

        # run detection
        detector.detect(det_obj)

        # Create a new dictionary and dump as json object
        d = {}
        d["type"] = "boundingBoxes"
        d["frameId"] = counter
        d["boxes"] = [b.rectangle for b in det_obj.bounding_boxes]
        j_string = json.dumps(d)

        # Write the JSON object to the file, add a comma and a newline
        if counter == vidstream.get_capture_length() - 1:
            outfile.writelines(j_string)
        else:
            outfile.writelines(j_string + ',\n')

        # Draw boxes and increment frame counter
        det_obj.draw_rectangles()
        counter += 1

        # Play the video in a window called "Output Video"
        try:
            cv2.imshow("Output Video", det_obj.frame)
        except OSError:
            # Figure out how to get Docker to use GUI
            print("Error displaying video. Are you running this in Docker perhaps?")

        # This next line is **ESSENTIAL** for the video to actually play
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    # End the list with a bracket, truncate file, then close it properly
    outfile.write("]")
    outfile.truncate()
    outfile.close()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
