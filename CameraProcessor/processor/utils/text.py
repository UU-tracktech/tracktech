"""Has functions that converts an object to a text.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import json


def bounding_boxes_to_json(bounding_boxes, timestamp) -> json:
    """Converts the bounding boxes to JSON format of API call.

    Args:
        bounding_boxes (BoundingBoxes): boxes that get converted to json.
        timestamp (Timestamp): timestamp of box used for syncing in interface.

    Returns:
        JSON representation of the object.
    """
    boxes_list = bounding_boxes.get_bounding_boxes()

    return json.dumps({
        "type": "boundingBoxes",
        "frameId": timestamp,
        "boxes": [__bounding_box_to_dict(bounding_box) for bounding_box in boxes_list],
    })


def __bounding_box_to_dict(bounding_box):
    """Converts the bounding_box to dict format according to API format.

    Args:
        bounding_box (BoundingBox): box that gets converted to json.

    Returns:
        str: JSON representation of the BoundingBox object.
    """
    res = {
            "boxId": bounding_box.get_identifier(),
            "rect": [
                bounding_box.get_rectangle().get_x1(),
                bounding_box.get_rectangle().get_y1(),
                bounding_box.get_rectangle().get_x2(),
                bounding_box.get_rectangle().get_y2()
            ],
            "objectType": bounding_box.get_classification()
        }

    if bounding_box.get_object_id() is not None:
        res["objectId"] = bounding_box.get_object_id()

    return res


def boxes_to_accuracy_json(bounding_boxes, image_id):
    """Converts the bounding boxes to JSON format of Accuracy.

      Args:
          bounding_boxes (BoundingBoxes): boxes that get converted to json.
          image_id (int): image_id of box used for accuracy calculations.

      Returns:
          JSON representation of the object.
      """
    boxes_list = bounding_boxes.get_bounding_boxes()

    return json.dumps({
        "imageId": image_id,
        "boxes": [__bounding_box_to_dict(bounding_box) for bounding_box in boxes_list],
    })

