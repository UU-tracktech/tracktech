"""Capable of displaying the separate stages in a single image.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import cv2

import processor.utils.draw as draw


def generate_tiled_image(frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes, dimensions=None):
    """Generates a tiled image with the following order left to right, top to bottom: raw, detection, tracking, Re-ID.

    Automatically downscales when the image is too big and there are no dimensions given.

    Args:
        frame_obj (FrameObj): Object containing the frame to draw in.
        detected_boxes (BoundingBoxes): Boxes generated by the detection algorithm.
        tracked_boxes (BoundingBoxes): Boxes generated by the tracking algorithm.
        re_id_tracked_boxes (BoundingBoxes): Boxes where re-id is performed after tracking.
        dimensions (int, int): New (width, height) of the image.

    Returns:
        numpy.ndarray: Tiled two by two image with new dimensions.
    """
    if dimensions is None:
        dimensions = __calculate_scaled_size(frame_obj.frame.shape)

    # The downscale image.
    scaled_frame = cv2.resize(frame_obj.frame, dimensions)

    # Draw detections boxes and downscale.
    detection_frame = frame_obj.frame.copy()
    draw.draw_detection_boxes(detection_frame, detected_boxes.bounding_boxes)
    detection_frame = cv2.resize(detection_frame, dimensions)

    # Draw tracking boxes and downscale.
    tracking_frame = frame_obj.frame.copy()
    draw.draw_tracking_boxes(tracking_frame, tracked_boxes.bounding_boxes)
    tracking_frame = cv2.resize(tracking_frame, dimensions)

    # Draw re-id boxes and downscale.
    re_id_frame = frame_obj.frame.copy()
    draw.draw_re_id_tracked_boxes(re_id_frame, re_id_tracked_boxes.bounding_boxes)
    re_id_frame = cv2.resize(re_id_frame, dimensions)

    # List representation of the images in 2D.
    list_2d = [[scaled_frame, detection_frame],
               [tracking_frame, scaled_frame]]

    # Return the tiled image.
    return cv2.vconcat([cv2.hconcat(list_h)
                       for list_h in list_2d])


def __calculate_scaled_size(shape):
    """Calculates the new shape of the image, downscaling dimensions that are too big.

    Args:
        shape (int, int, int): height, width, depth of the frame.

    Returns:
        (int, int): scaled (width, height) of image.
    """
    height, width, _ = shape

    # Downscale width at least to 900.
    if width > 900:
        width_scaling = 900 / width
        width = width * width_scaling
        height = height * width_scaling

    # Downscale height to a maximum of 430.
    if height > 430:
        height_scaling = 430 / height
        width = width * height_scaling
        height = height * height_scaling

    # Set scaled size.
    return int(width), int(height)
