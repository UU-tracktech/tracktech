"""Tests the test.py functions in utils.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json
from processor.utils.text import bounding_boxes_to_json, boxes_to_accuracy_json, boxes_to_txt, error_to_json
from processor.data_object.bounding_boxes import BoundingBoxes


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

    def test_boxes_to_txt(self, bbox, img):
        """Tests the boxes_to_txt function.

        Args:
            bbox (BoundingBox): the bounding box fixture.
            img (np.ndarray): the image fixture.
        """
        txt_string = boxes_to_txt([bbox], (img.shape[0], img.shape[1]), 1)
        assert txt_string == "1,1,60,120,60,60,1,1,0.50 \n"

    def test_error_to_json(self):
        """Tests the error_to_json function."""
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
