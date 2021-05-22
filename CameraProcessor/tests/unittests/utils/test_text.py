"""Tests the test.py functions in utils

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json
from processor.utils.text import bounding_boxes_to_json, boxes_to_accuracy_json
from processor.data_object.bounding_boxes import BoundingBoxes


class TestText:
    """Class that holds the functions to test text.py
    """

    def test_bounding_boxes_to_json(self, bbox):
        """Function to test the bounding_boxes_to_json function

        Args:
            bbox (BoundingBox): bounding box fixture
        """
        bboxes = BoundingBoxes([bbox])
        json_string = bounding_boxes_to_json(bboxes, 1)
        proper_string = json.dumps({"type": "boundingBoxes",
                                    "frameId": 1,
                                    "boxes": [
                                        {"boxId": 1,
                                         "rect": [bbox.get_rectangle().get_x1(),
                                                  bbox.get_rectangle().get_x2(),
                                                  bbox.get_rectangle().get_y1(),
                                                  bbox.get_rectangle().get_y2()]
                                         }
                                    ]
                                    })
        assert json_string == proper_string

    def test_boxes_to_txt(self, bbox, img):
        """Tests the boxes_to_txt function

        Args:
            bbox (BoundingBox): the bounding box fixture
            img (np.ndarray): the image fixture
        """
        txt_string = boxes_to_accuracy_json([bbox], (img.shape[0], img.shape[1]), 1)
        assert txt_string == "1,1,60,120,60,60,1,1,1 \n"
