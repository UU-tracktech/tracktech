# Determine training set
# Determine test set
# Verification sets

# Run test set in epochs

# Determine accuracy of a bounding box estimate
import os
import logging
from typing import List, Any, Union

from podm.podm import BoundingBox, get_pascal_voc_metrics
import configparser
from processor.pipeline.detection.bounding_box import BoundingBox as bounding_box
import sys
import cv2
import podm.podm
from processor.input.image_capture import ImageCapture
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.training.pre_annotations import PreAnnotations

class AccuracyObject:

    def parseboxes(self, boxes_to_parse):
        list_parsed_boxes: List[BoundingBox] = []
        for t in range(len(boxes_to_parse)):
            boxes = boxes_to_parse[t]
            for box in boxes:
                width = box.rectangle[2]
                height = box.rectangle[3]
                parsedbox = BoundingBox(label="undefined", xtl=box.rectangle[0]/10000, ytl=box.rectangle[1]/10000,
                                        xbr=width/10000, ybr=height/10000, image_name=str(t), score=box.certainty)
                list_parsed_boxes.append(parsedbox)
        return list_parsed_boxes

    def readboxes(self, dirImage, pathToBoxes):
        capture = ImageCapture(dirImage)
        bounding_boxes_annotations = PreAnnotations(pathToBoxes, capture.nr_images)
        bounding_boxes_annotations.parse_file()
        bounding_boxes = bounding_boxes_annotations.boxes
        return self.parseboxes(bounding_boxes)

    def detect(self, det_dir):
        bounding_boxes_path_mock = f'{self.root_dir}/data/annotated/{self.folder_name}/{det_dir}'
        boundingboxes_det = self.readboxes(self.images_dir, bounding_boxes_path_mock)

        self.result = get_pascal_voc_metrics(self.boundingboxes_gt, boundingboxes_det, self.iou_threshold)

        tps = 0
        for key in self.result.keys():
            tps += self.result[key].tp

        print("tp (all classes): " + str(tps))
        print("accuracy: " + str(self.result['undefined'].tp / len(boundingboxes_det)))
        print("tp (only undefined): " + str(self.result['undefined'].tp))
        print("fp: " + str(self.result['undefined'].fp))

    def __init__(self, root_dir, folder_name, gt_dir):
        self.root_dir = root_dir
        self.folder_name = folder_name
        self.gt_dir = gt_dir
        self.images_dir = f'{root_dir}/data/annotated/{folder_name}/img1'

        bounding_boxes_path_gt = f'{root_dir}/data/annotated/{folder_name}/{gt_dir}'

        self.boundingboxes_gt = self.readboxes(self.images_dir, bounding_boxes_path_gt)

        configs = configparser.ConfigParser(allow_no_value=True)
        configs.read(f'{root_dir}/configs.ini')
        yolo_config = configs['Yolov5']

        self.iou_threshold = float(yolo_config['iou-thres'])


dir_to_root = os.path.abspath(__file__ + '/../../../../')
object = AccuracyObject(os.path.abspath(__file__ + '/../../../../'), 'test', 'gt/gt.txt')
object.detect('mockyolo/gt.txt')

#        bounding_boxes_path_mock = f'{root_dir}/data/annotated/{folder_name}/mockyolo/gt.txt'
#        boundingboxes_det = readboxes(images_dir, bounding_boxes_path_mock)

#for line in lines:
#    (frame_nr, person_id, x, y, w, h) = [int(i) for i in line.split(delimiter)[:6]]
#    box = BoundingBox(label="undefined", image_name=str(frame_nr), xtl=x, ytl=y, xbr=w, ybr=h)
#    if len(boundingboxes_gt) < frame_nr:
#        boundingboxes_gt.append([])
#    boxes = boundingboxes_gt[frame_nr - 1]
#    if boxes.count == 0:
#        boundingboxes_gt[frame_nr - 1] = [box]
#    else:
#        boundingboxes_gt[frame_nr - 1].append(box)

#for boxes in bounding_boxes_gt:
#    parsedBoxes = []
#    for box in boxes:
#        width = box.rectangle[2] - box.rectangle[0]
#        height = box.rectangle[3] - box.rectangle[1]
#        parsedBox = BoundingBox(label="undefined", xtl=box.rectangle[0], ytl=box.rectangle[1], xbr=width,
#                                ybr=height, image_name=box.identifier)
#        parsedBoxes.append(parsedBox)
#    boundingboxes_gt.append(parsedBoxes)

#root_dir = os.path.abspath(__file__ + '/../../../../')
#logging.basicConfig(filename=os.path.join(root_dir, 'app.log'), filemode='w',
#                    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
#                    level=logging.INFO,
#                    datefmt='%Y-%m-%d %H:%M:%S')
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

#folder_name = 'test'
#images_dir = f'{root_dir}\\data\\annotated\\{folder_name}\\img1'
#bounding_boxes_path = f'{root_dir}\\data\\annotated\\{folder_name}\\gt'
#bounding_boxes_path_mock = f'{root_dir}\\data\\annotated\\{folder_name}\\mockyolo'

#capture_gt = ImageCapture(images_dir)
#capture_mock = ImageCapture(images_dir)
#bounding_boxes_gt = PreAnnotations(bounding_boxes_path, capture_gt.nr_images).boxes
#bounding_boxes_mock = PreAnnotations(bounding_boxes_path_mock, capture_mock.nr_images).boxes

#logging.info('start training')
#tp = 0
#fp = 0
#fn = 0
#frame_index = 0




#def iou(boundingbox_gt, boundingbox_pred, threshold=0.5):
#    return True


#while capture_gt.opened() and capture_mock.opened():
#    ret_gt, frame_gt = capture_gt.get_next_frame()
#    ret_mock, frame_mock = capture_mock.get_next_frame()
#
#    if not capture_mock.nr_images == capture_gt.nr_images:
#        break

#    if not (ret_gt or ret_mock):
#        logging.warning('ret_gt: ' + ret_gt + '\n ret_mock: ' + ret_mock)
#        continue

#    boundingbox_difference = len(bounding_boxes_gt[frame_index]) - len(bounding_boxes_mock[frame_index])
#    if boundingbox_difference < 0:
#        fp -= boundingbox_difference
#    else:
#        fn += boundingbox_difference

    # Close loop when q is pressed
#    if cv2.waitKey(30) & 0xFF == ord('q'):
#        break
#    frame_index += 1
#logging.info('training stopping')
# When everything is done release the capture
#capture_gt.close()
