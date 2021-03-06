"""Has the functions that converts an object to a text.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import json


def feature_map_to_json(feature_map=None, object_id=None):
    """Sends a feature_map to the orchestrator.

    Args:
        feature_map ([Float]): An array of numerical values.
        object_id (Int): The object where the feature_map refers too.

    Returns:
        json: Json message of the featuremap.
    """
    # Parses a feature map into a json message.
    return json.dumps({
        "type": "featureMap",
        "objectId": object_id,
        "featureMap": feature_map
    })


def bounding_boxes_to_dict(bounding_boxes, timestamp):
    """Converts a BoundingBoxes to a dictionary according to API format.

    Args:
        bounding_boxes (BoundingBoxes): boxes that get converted to json.
        timestamp (Timestamp): timestamp of boxes used for syncing in the interface.

    Returns:
        dict: Representation of the BoundingBoxes object.
    """
    return {
        'type': 'boundingBoxes',
        'frameId': timestamp,
        'boxes': [bounding_box_to_dict(bounding_box) for bounding_box in bounding_boxes],
    }


def bounding_box_to_dict(bounding_box):
    """Converts the bounding_box to dict format according to API format.

    Args:
        bounding_box (BoundingBox): box that gets converted to json.

    Returns:
        dict: Representation of the BoundingBox object.
    """
    res = {
        'boxId': bounding_box.identifier,
        'rect': [
            bounding_box.rectangle.x1,
            bounding_box.rectangle.y1,
            bounding_box.rectangle.x2,
            bounding_box.rectangle.y2
        ],
        'objectType': bounding_box.classification,
        'certainty': bounding_box.certainty
    }

    # Add the objectId to the dict if it is set.
    if bounding_box.object_id is not None:
        res['objectId'] = bounding_box.object_id

    return res


def boxes_to_accuracy_json(bounding_boxes, image_id):
    """Converts the bounding boxes to JSON format of Accuracy.

      Args:
          bounding_boxes (BoundingBoxes): boxes that get converted to json.
          image_id (int): image_id of box used for accuracy calculations.

      Returns:
          (json): JSON representation of the object.
      """
    return json.dumps({
        'imageId': image_id,
        'boxes': [bounding_box_to_dict(bounding_box) for bounding_box in bounding_boxes],
    })


def boxes_to_txt(bounding_boxes, shape, frame_nr):
    """Write the detection object to a txt file, so that accuracy testing can read it.

    Args:
        bounding_boxes (List[BoundingBox]): list of bounding boxes.
        shape (int, int): shape of frame.
        frame_nr (int): number of frame.

    Returns:
        str: Boxes in string format with comma separation
    """
    boxes_text_string = ""
    width, height = shape

    for bounding_box in bounding_boxes:
        boxes_text_string += \
            f'{frame_nr},{bounding_box.identifier},' \
            f'{int(bounding_box.rectangle.x1 * width)},' \
            f'{int(bounding_box.rectangle.y1 * height)},' \
            f'{int((bounding_box.rectangle.x2 - bounding_box.rectangle.x1) * width)},' \
            f'{int((bounding_box.rectangle.y2 - bounding_box.rectangle.y1) * height)},' \
            f'1,1,{"%.2f" % round(float(bounding_box.certainty), 2)} \n'  # certainty rounded to two decimals

    return boxes_text_string
