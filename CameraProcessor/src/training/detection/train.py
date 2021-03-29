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


capture = ImageCapture(images_dir)
bounding_boxes = PreAnnotations(bounding_boxes_path, capture.nr_images).boxes

logging.info('start training')
while capture.opened():
    ret, frame = capture.get_next_frame()

    if not ret:
        logging.warning('Frame inside training not found')
        continue

    # Create detectionObj
    detection_obj = DetectionObj(None, frame, capture.image_index)
    # Run detection on object
    detection_obj.bounding_box = bounding_boxes[capture.image_index]
    # Visualise rectangles and show it
    detection_obj.draw_rectangles()
    cv2.imshow('Frame', detection_obj.frame)

    # Close loop when q is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

logging.info('training stopping')
# When everything is done release the capture
capture.close()
