"""Gives a way to have the data stream written to a json file to help repeating

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
# import time
# import os
# import sys
# import json
# import configparser
# import cv2
#
# from absl import app
# from processor.pipeline.detection.yolov5_runner import Yolov5Detector
# from processor.input.video_capture import VideoCapture
# from tests.conftest import root_path
#
# sys.path.insert(0, os.path.join(root_path, 'processor/pipeline/detection/yolov5'))
#
#
# # pylint: disable=duplicate-code
# def main(_argv):
#     """Runs YOLOv5 detection on a videofile specified in line 33
#     and saves the JSON objecs to testdata/output.json
#     """
#     # Load the config file, take the relevant Yolov5 section
#     configs = configparser.ConfigParser(allow_no_value=True)
#     configs.read(os.path.join(root_path, 'configs.ini'))
#     trueconfig = configs['Yolov5']
#     filterconfig = configs['Filter']
#
#     local_time = time.localtime()
#
#     # Instantiate the Detection Object
#     det_obj = DetectionObj(local_time, None, 0)
#
#     # Capture the video stream
#     vidstream = VideoCapture(os.path.join(root_path, "/data/videos/test.mp4"))
#
#     # Instantiate the detector
#     print("Instantiating detector...")
#     detector = Yolov5Detector(trueconfig, filterconfig)
#
#     # Open Json file, go to 0th line to overwrite
#     outfile = open("testdata/output.json", "w")
#     outfile.seek(0)
#     outfile.write("[")
#
#     # Frame counter starts at 0. Will probably work differently for streams
#     print("Starting video stream...")
#     counter = 0
#     while vidstream.opened():
#         # Set the detected bounding box list to empty
#         det_obj.bounding_box = []
#         ret, frame, _ = vidstream.get_next_frame()
#
#         if not ret:
#             if counter == vidstream.get_capture_length():
#                 print("End of file")
#             else:
#                 raise ValueError("Feed has been interrupted")
#             break
#
#         # update frame, frame number, and time
#         det_obj.frame = frame
#         det_obj.frame_nr = counter
#         det_obj.timestamp = time.localtime()
#
#         # run detection
#         detector.detect(det_obj)
#
#         # Create a new dictionary and dump as json object
#         json_obj = {}
#         json_obj["type"] = "boundingBoxes"
#         json_obj["frameId"] = counter
#         json_obj["boxes"] = [b.rectangle for b in det_obj.bounding_boxes]
#         j_string = json.dumps(json_obj)
#
#         # Write the JSON object to the file, add a comma and a newline
#         if counter == vidstream.get_capture_length() - 1:
#             outfile.writelines(j_string)
#         else:
#             outfile.writelines(j_string + ',\n')
#
#         # Draw boxes and increment frame counter
#         det_obj.draw_rectangles()
#         counter += 1
#
#         # Play the video in a window called "Output Video"
#         try:
#             cv2.imshow("Output Video", det_obj.frame)
#         except OSError:
#             # Figure out how to get Docker to use GUI
#             print("Error displaying video. Are you running this in Docker perhaps?")
#
#         # This next line is **ESSENTIAL** for the video to actually play
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             return
#
#     # End the list with a bracket, truncate file, then close it properly
#     outfile.write("]")
#     outfile.truncate()
#     outfile.close()
#
#
# if __name__ == '__main__':
#     try:
#         app.run(main)
#     except SystemExit:
#         pass
