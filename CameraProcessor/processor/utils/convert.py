"""Has functions that converts an object to a dictionary for the frame buffer.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


def to_buffer_dict(frame_obj, bounding_boxes):
    """Turn FrameObj and BoundingBoxes into dictionary usable by frame buffer.

    Args:
        frame_obj (FrameObj): information object containing the OpenCV frame and timestamp.
        bounding_boxes (BoundingBoxes): information object containing list of bounding boxes.

    Returns:
        dict: dictionary containing all necessary frame and bounding boxes information for the buffer.
    """
    return {
        "frame": frame_obj.get_frame(),
        "frameId": frame_obj.get_timestamp(),
        "boxes": [
            {
                "boxId": bounding_box.get_identifier(),
                "rect": bounding_box.get_rectangle()
            }
            for bounding_box in bounding_boxes.get_bounding_boxes()
        ]
    }