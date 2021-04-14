import cv2
import os
import logging
import sys
from src.input.image_capture import ImageCapture
from src.pipeline.detection.detection_obj import DetectionObj
from src.training.pre_annotations import PreAnnotations

root_dir = os.path.abspath(__file__ + '/../../../../')
logging.basicConfig(filename=os.path.join(root_dir, 'app.log'), filemode='w',
                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

folder_name = 'test'
gt = f'{root_dir}/data/annotated/{folder_name}/gt/gt.txt'
gt_accuracy = f'{root_dir}/data/annotated/{folder_name}/gt/gt_accuracy.txt'
global skipped_lines
# Read file
with open(gt) as file:
    lines = [line.rstrip('\n') for line in file]

# Determine delimiter automatically
delimiter = ' '
if lines[0].__contains__(','):
    delimiter = ','

newData = ""

# The X and Y of the ground truth boundingboxes are sometimes negative
for line in lines:
    (frame_nr, person_id, x, y, w, h) = [int(i) for i in line.split(delimiter)[:6]]
    parsed_box = "undefined " + str(x) + ' ' + str(y) + ' ' + str(x + w) + ' ' + str(x + h)
    newData += parsed_box + '\n'

gt_accuracy_file = open(gt_accuracy, "w")
gt_accuracy_file.write(newData)



