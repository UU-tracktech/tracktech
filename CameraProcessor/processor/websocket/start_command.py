"""Contains StartCommand class which holds information to start tracking.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import base64
import cv2
import numpy as np

from processor.utils.features import slice_bounding_box


class StartCommand():
    """StartCommand class that stores data regarding which object to start tracking"""
    def __init__(self, object_id, image=None, frame_id=None, box_id=None):
        """Constructor for the StopCommand class. A start command either contains a cutout,
           a combination of frame_id and box_id, or both.

        Args:
            object_id (int): Identifier of the object to be followed.
            image (image): URL encoded cutout of the object to be followed.
            frame_id (int): The id of the frame in the frame buffer
            box_id (int): the id of the box in the frame defined by the frame buffer
        """
        if not isinstance(object_id, int):
            raise TypeError("Object id should be an integer")

        if not isinstance(frame_id, float):
            raise TypeError("Frame id should be a float")

        if not isinstance(box_id, int):
            raise TypeError("Box id should be an integer")

        # Set the cutout to none
        self.__cutout = None

        # Convert the cutout (if it exist), to an openCV image, rather than a base 64 encoded image.
        if image is not None:
            self.__image = self.__convert_base64_image_to_np_array(image)
        else:
            self.__image = None

        self.__object_id = object_id
        self.__box_id = box_id
        self.__frame_id = frame_id

    def get_cutout(self, framebuffer):
        """ Tries to get the cutout from the information in the StartCommand, either from the frame buffer
        if that is possible, otherwise directly from the sent image if that is possible, and otherwise
        raise an error and don't follow the subject.

        Args:
            framebuffer (FrameBuffer) frame buffer object that contains

        Returns:

        """
        # Try to find the frame in the frame buffer if it was not already found before.
        error = None
        if self.__cutout is None:
            if self.__frame_id is not None and self.__box_id is not None:
                try:
                    stored_frame = framebuffer.get_frame(self.__frame_id).frame
                    stored_box = framebuffer.get_box(self.__frame_id, self.__box_id)
                    self.__cutout = slice_bounding_box(stored_box, stored_frame)
                    return self.__cutout
                except ValueError as value_error:
                    error = value_error
                # Frame could not be found in the frame buffer, it was probably too small.
                except IndexError as index_error:
                    error = index_error
            # We can still get the data from the image.
            if self.__image is not None:
                self.__cutout = self.__image
            # There is no way to get the image. Log this and don't use the tracking data.
            if error is not None:
                raise error

        # If the cutout was already found in the frame buffer before (or not found and taken from image),
        # don't try to find it again.
        return self.__cutout

    @staticmethod
    def __convert_base64_image_to_np_array(image):
        """ Converts the base64 encoded image from the websocket to a np array usable by OpenCV.

        Args:
            cutout (string): a string of the image in base64 png format

        Returns:

        """
        # Extract features from image.
        encoded_data = base64.b64decode(image.split(',')[1])
        decoded_image = cv2.imdecode(np.fromstring(encoded_data, np.uint8), cv2.IMREAD_COLOR)
        return cv2.cvtColor(decoded_image, cv2.COLOR_RGBA2RGB)

    @staticmethod
    def from_message(message):
        if "objectId" not in message.keys():
            raise KeyError("objectId missing")

        # The start command should at least contain either a cutout, or a box_id and frame_id
        # Otherwise, there is not enough data to generate a cutout
        if "image" not in message.keys() and ("boxId" not in message.keys() or "frameId" not in message.keys()):
            raise KeyError("Not enough data for cutout in message")

        object_id = message["objectId"]

        # These could all possibly none
        image = message.get("image", None)
        box_id = message.get("boxId", None)
        frame_id = message.get("frameId", None)
        return StartCommand(object_id, image, frame_id, box_id)

    @property
    def object_id(self):
        return self.__object_id

    @property
    def image(self):
        return self.__image

    @property
    def box_id(self):
        return self.__box_id

    @property
    def frame_id(self):
        return self.__frame_id

    def __eq__(self, other):
        return [self.__object_id == other.object_id,
                self.__image == other.image,
                self.box_id == other.box_id,
                self.frame_id == other.frame_id]

    def __repr__(self):
        return f"StartCommand(object id: {self.__object_id} image: " \
               f"{self.__image if self.__image is not None else 'None'} " \
               f"box id: {self.__box_id if self.__box_id is not None else 'None'} " \
               f"frame id: {self.__frame_id if self.frame_id is not None else 'None'})"

