import os
import logging
import sys
import cv2
from processor.input.image_capture import ImageCapture
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.training.pre_annotations import PreAnnotations

root_dir = os.path.abspath(__file__ + '/../../../../')
logging.basicConfig(filename=os.path.join(root_dir, 'app.log'), filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

folder_name = 'test'
det = f'{root_dir}/data/annotated/{folder_name}/det/det.txt'
det_accuracy = f'{root_dir}/data/annotated/{folder_name}/det/det_accuracy.txt'
global skipped_lines
# Read file
with open(det) as file:
    lines = [line.rstrip('\n') for line in file]

# Determine delimiter automatically
delimiter = ' '
if lines[0].__contains__(','):
    delimiter = ','

newData = ""

# The X and Y of the ground truth boundingboxes are sometimes negative
for line in lines:
    (frame_nr, person_id, x, y, w, h, conf) = [float(i) for i in line.split(delimiter)[:7]]
    parsed_box = "undefined " + str(1) + ' ' + str(int(x)) + ' ' + str(int(y)) + ' ' + str(int(x + w)) + ' ' + str(int(x + h))
    if frame_nr == 1:
        newData += parsed_box + '\n'

det_accuracy_file = open(det_accuracy, "w")
det_accuracy_file.write(newData)