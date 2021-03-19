# Determine training set
# Determine test set
# Verification sets

# Run test set in epochs

# Determine accuracy of a bounding box estimate
import cv2
import os
from detection.dectection_obj import DetectionObj
from training.annotations_obj import Annotations

working_dir = os.path.normpath(os.getcwdb())
print(working_dir)
# folder_path = os.path.join(working_dir.parent.parent, "data\\annotated\\test")
folder_path = "C:\\Users\\Gerar\\OneDrive - Universiteit Utrecht\\Documents\\University\\3.3 Bachelorproject\\TrackTech\\CameraProcessor\\data\\annotated"


for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)

    if os.path.isfile(item_path):
        continue

    frame_nr = 0
    images_dir = os.path.join(item_path, "img1")

    bounding_boxes_path = os.path.join(item_path, "gt")
    nr_images = len(os.listdir(images_dir))
    bounding_boxes = Annotations(bounding_boxes_path, nr_images).boxes

    for image_name in sorted(os.listdir(images_dir)):
        frame = cv2.imread(os.path.join(images_dir, image_name))

        # Create detectionObj
        detection_obj = DetectionObj(None, frame, frame_nr)
        # Run detection on object
        detection_obj.bounding_box = bounding_boxes[frame_nr]
        # Visualise rectangles and show it
        detection_obj.draw_rectangles()
        cv2.imshow('Frame', detection_obj.frame)

        # Close loop when q is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        frame_nr += 1


# When everything is done release the capture
cv2.destroyAllWindows()
