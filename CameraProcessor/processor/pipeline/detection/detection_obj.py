"""Contains the detection object class

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json
import cv2


class DetectionObj:
    """Object that holds all the bounding boxes for a specific frame
    """

    def __init__(self, timestamp, frame, frame_nr):
        self.timestamp = timestamp
        self.frame = frame
        self.frame_nr = frame_nr
        self.bounding_boxes = []

    def draw_rectangles(self) -> None:
        """Draws the bounding boxes on the frame.
        """
        red = (0, 0, 255)
        for bounding_box in self.bounding_boxes:
            height, width, _ = self.frame.shape
            # Object bounding box.
            cv2.rectangle(self.frame,
                          (int(bounding_box.rectangle[0] * width),
                           int(bounding_box.rectangle[1] * height)),
                          (int(bounding_box.rectangle[2] * width),
                           int(bounding_box.rectangle[3] * height)),
                          red,
                          2
                          )

            # Tag background.
            cv2.rectangle(self.frame,
                          (int(bounding_box.rectangle[0] * width),
                           int(bounding_box.rectangle[1] * height) - 35),
                          (int(bounding_box.rectangle[0] * width + (len(bounding_box.classification) + 4) * 15),
                           int(bounding_box.rectangle[1] * height)),
                          red,
                          -1
                          )

            # Tag with confidence.
            cv2.putText(self.frame,
                        f'{bounding_box.classification} {round(float(bounding_box.certainty), 2)} ',
                        (int(bounding_box.rectangle[0] * width),
                         int(bounding_box.rectangle[1] * height) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 0, 0),
                        2
                        )

        return self.frame

    def to_json(self) -> json:
        """Converts the object to JSON format.

        Returns:
            JSON representation of the object.
        """
        return json.dumps({
            "type": "boundingBoxes",
            "frameId": self.timestamp,
            "boxes": [bounding_box.to_dict() for bounding_box in self.bounding_boxes],
        })

    def to_txt_file(self, dest):
        """Write the detection object to a txt file, so that accuracy testing can read it.

        Args:
            dest: Filepath (including file name)

        """
        detection_obj_as_txt = ""
        for bounding_box in self.bounding_boxes:
            height, width, _ = self.frame.shape
            detection_obj_as_txt += (
                f'{self.frame_nr},{bounding_box.identifier},'
                f'{int(bounding_box.rectangle[0] * width)}, '
                f'{int(bounding_box.rectangle[1] * height)},'
                f'{int((bounding_box.rectangle[2] - bounding_box.rectangle[0]) * width)}, '
                f'{int((bounding_box.rectangle[3] - bounding_box.rectangle[1]) * height)},1,1,1 \n')
        try:
            file = open(dest, 'a')
            file.write(detection_obj_as_txt)
            file.close()
        except RuntimeError:
            print(f'{dest}: Cannot write to this file')
