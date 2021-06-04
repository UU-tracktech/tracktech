"""Contains logic to draw the boxes on the frame, tags depend on what type of box it is.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import random
import cv2


def draw_bounding_boxes(frame, bounding_boxes):
    """Draws the bounding boxes on the frame.

    Args:
        frame (numpy.ndarray): Frame the bounding boxes get drawn on.
        bounding_boxes ([BoundingBox]): List of bounding boxes that get drawn.
    """
    # Color and shape.
    red = (0, 0, 255)

    # Draw each box on frame.
    for bounding_box in bounding_boxes:
        __draw_box(frame, bounding_box, red)


def draw_detection_boxes(frame, bounding_boxes):
    """Draws the detection boxes on top of the frame displaying the classification and certainty.

    Args:
        frame (numpy.ndarray): Frame the bounding boxes get drawn on.
        bounding_boxes ([BoundingBox]): List of bounding boxes that get drawn.
    """
    # Draw each box on the frame with tag.
    for bounding_box in bounding_boxes:
        color = __generate_random_color(bounding_box.classification)
        __draw_box(frame, bounding_box, color)

        __draw_text(
            frame,
            bounding_box,
            f'{bounding_box.classification} {round(float(bounding_box.certainty), 2)}',
            color
        )


def draw_tracking_boxes(frame, bounding_boxes):
    """Draws the tracking boxes on top of the frame using the identifier.

    Args:
        frame (numpy.ndarray): Frame the bounding boxes get drawn on.
        bounding_boxes ([BoundingBox]): List of bounding boxes that get drawn.
    """
    # Draw each box on frame with identifier tag.
    for bounding_box in bounding_boxes:
        # Generate random color based on identifier.
        color = __generate_random_color(bounding_box.identifier)

        __draw_box(frame, bounding_box, color)

        __draw_text(frame, bounding_box, f'{bounding_box.identifier}', color)


# pylint: disable=unnecessary-pass, unused-argument
def draw_re_id_tracked_boxes(frame, bounding_boxes):
    """Draws the re-id boxes on top of the frame.

    Args:
        frame (numpy.ndarray): Frame the bounding boxes get drawn on.
        bounding_boxes (List[BoundingBox]): List of bounding boxes that get drawn.
    """

    pass


def __draw_box(frame, bounding_box, color):
    """Draws one bounding box on the frame.

    Args:
        frame (numpy.ndarray): frame the box is drawn on.
        bounding_box (BoundingBox): Bounding box itself.
        color (int, int, int): Color of the BoundingBox.
    """
    height, width, _ = frame.shape

    # Draw bounding box.
    cv2.rectangle(
        frame,
        (int(bounding_box.rectangle.x1 * width), int(bounding_box.rectangle.y1 * height)),
        (int(bounding_box.rectangle.x2 * width), int(bounding_box.rectangle.y2 * height)),
        color,
        2
    )


def __draw_text(frame, bounding_box, text, color):
    """Draw text at top left corner of the Bounding box given a certain color.

    Args:
        frame (numpy.ndarray): frame the box is drawn on.
        bounding_box (BoundingBox): Bounding box itself.
        text (str): String of text that gets displayed.
        color (int, int, int): Color of the tag background.
    """
    # Shape.
    height, width, _ = frame.shape

    # Pre-scaled coordinates.
    scaled_x1 = bounding_box.rectangle.x1 * width
    scaled_y1 = bounding_box.rectangle.y1 * height

    # Draw filled rectangle to place text on.
    cv2.rectangle(
        frame,
        (int(scaled_x1) - 1, int(scaled_y1) - 38),
        (int(scaled_x1 + len(text) * 15), int(scaled_y1)),
        color,
        -1
    )

    # Draw text.
    cv2.putText(
        frame,
        text,
        (int(scaled_x1), int(scaled_y1) - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        2
    )


def __generate_random_color(identifier):
    """Generate the color using the identifier as unique hash.

    Args:
        identifier (int): Unique identifier on which color is generated.

    Returns:
        (int, int, int): BGR color value.
    """
    random.seed(identifier)
    return random.sample(range(10, 255), 3)
