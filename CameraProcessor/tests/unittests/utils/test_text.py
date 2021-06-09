"""Tests the test.py functions in utils.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json
from processor.utils.text import bounding_boxes_to_json, boxes_to_accuracy_json, boxes_to_txt, error_to_json, \
                                 feature_map_to_json, bounding_box_to_dict
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.rectangle import Rectangle


class TestText:
    """Class that holds the functions to test text.py."""
    def test_bounding_boxes_to_json(self, bbox):
        """Function to test the bounding_boxes_to_json function.

        Args:
            bbox (BoundingBox): bounding box fixture
        """
        bboxes = BoundingBoxes([bbox])
        json_string = bounding_boxes_to_json(bboxes, 1)
        proper_string = json.dumps({"type": "boundingBoxes",
                                    "frameId": 1,
                                    "boxes": [
                                        {
                                            "boxId": 1,
                                            "rect": [
                                                bbox.rectangle.x1,
                                                bbox.rectangle.x2,
                                                bbox.rectangle.y1,
                                                bbox.rectangle.y2
                                            ],
                                            "objectType": bbox.classification,
                                            "certainty": bbox.certainty
                                         }
                                    ]
                                    })
        assert json_string == proper_string

    def test_feature_map_to_json(self):
        """Tests feature_map_to_json."""
        fm = feature_map_to_json([0.9, 0.8, 0.7, 0.6, 0.5], 1)
        json_fm = json.dumps({
            "type": "featureMap",
            "objectId": 1,
            "featureMap": [0.9, 0.8, 0.7, 0.6, 0.5]
        })
        assert fm == json_fm

    def test_bounding_box_to_dict(self):
        """Tests bounding_box_to_dict."""
        box1 = BoundingBox(1, Rectangle(0, 0.5, 0.75, 1), "person", 0.5, object_id=5)
        box1_dict = {'boxId': 1,
                     'certainty': 0.5,
                     'objectId': 5,
                     'objectType': 'person',
                     'rect': [0, 0.5, 0.75, 1]}
        assert bounding_box_to_dict(box1) == box1_dict

    def test_boxes_to_txt(self, bbox, img):
        """Tests the boxes_to_txt function.

        Args:
            bbox (BoundingBox): the bounding box fixture.
            img (np.ndarray): the image fixture.
        """
        txt_string = boxes_to_txt([bbox], (img.shape[0], img.shape[1]), 1)
        assert txt_string == "1,1,60,120,60,60,1,1,0.50 \n"

    def test_error_to_json(self):
        """Tests the error_to_json function.
        """
        error_message = error_to_json(NameError("Testing"))
        assert error_message == '''{"type": "error", "error": "NameError('Testing')"}'''

    def test_boxes_to_accuracy_json(self, bbox):
        """Tests the boxes_to_accuracy_json function.

        Args:
            bbox (BoundingBox): the bounding box fixture.
        """
        json_string = boxes_to_accuracy_json(BoundingBoxes([bbox]), 1)
        proper_string = json.dumps({"imageId": 1,
                                    "boxes": [
                                        {
                                            "boxId": bbox.identifier,
                                            "rect": [
                                                bbox.rectangle.x1,
                                                bbox.rectangle.x2,
                                                bbox.rectangle.y1,
                                                bbox.rectangle.y2
                                            ],
                                            "objectType": bbox.classification,
                                            "certainty": 0.5
                                         }
                                    ]
                                    })
        assert json_string == proper_string
