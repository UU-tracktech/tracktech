import os
import cv2


def is_same_frame_image(original, second):
    """Checks if two frames images are the same

    Args:
        original (Frame): Original frame
        second (Frame): Frame to compare the original frame to

    Returns:
        (bool): Whether two frames are the same
    """
    # Calculate difference
    difference = cv2.subtract(original, second)
    b, g, r = cv2.split(difference)

    # Return true if it is the same image
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    return False


def get_sample_frame():
    """So the test has access to an example frame in the detection object

    Returns (frame):
        Opencv frame from test data
    """
    __root_dir = os.path.abspath(os.path.join(__file__, '../../../'))
    __images_name = f'{__root_dir}/data/annotated/test/img1/000001.jpg'
    return cv2.imread(__images_name)
