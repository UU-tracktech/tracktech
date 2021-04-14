# Determine training set
# Determine test set
# Verification sets

# Run test set in epochs

# Determine accuracy of a bounding box estimate
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
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

folder_name = 'test'
images_dir = f'{root_dir}\\data\\annotated\\{folder_name}\\img1'
bounding_boxes_path = f'{root_dir}\\data\\annotated\\{folder_name}\\gt'
bounding_boxes_path_mock = f'{root_dir}\\data\\annotated\\{folder_name}\\mockyolo'

capture_gt = ImageCapture(images_dir)
capture_mock = ImageCapture(images_dir)
bounding_boxes_gt = PreAnnotations(bounding_boxes_path, capture_gt.nr_images).boxes
bounding_boxes_mock = PreAnnotations(bounding_boxes_path_mock, capture_mock.nr_images).boxes

logging.info('start training')
tp = 0
fp = 0
fn = 0
frame_index = 0




def iou(boundingbox_gt, boundingbox_pred, threshold=0.5):
    return True


while capture_gt.opened() and capture_mock.opened():
    ret_gt, frame_gt = capture_gt.get_next_frame()
    ret_mock, frame_mock = capture_mock.get_next_frame()

    if not capture_mock.nr_images == capture_gt.nr_images:
        break

    if not (ret_gt or ret_mock):
        logging.warning('ret_gt: ' + ret_gt + '\n ret_mock: ' + ret_mock)
        continue

    boundingbox_difference = len(bounding_boxes_gt[frame_index]) - len(bounding_boxes_mock[frame_index])
    if boundingbox_difference < 0:
        fp -= boundingbox_difference
    else:
        fn += boundingbox_difference

    # Close loop when q is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    frame_index += 1
logging.info('training stopping')
# When everything is done release the capture
capture_gt.close()
