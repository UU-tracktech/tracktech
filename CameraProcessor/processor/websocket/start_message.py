"""Contains StartMessage class which holds information to start tracking.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import base64
import cv2
import numpy as np

from processor.utils.features import slice_bounding_box
from processor.websocket.i_message import IMessage


class StartMessage(IMessage):
    """StartMessage class that stores data regarding which object to stop tracking."""

    def __init__(self, object_id, image=None, frame_id=None, box_id=None):
        """Constructor for the StopMessage class.

        A start command either contains a cutout, a combination of frame_id and box_id, or both.

        Args:
            object_id (int): Identifier of the object to be followed.
            image (image/None): URL encoded cutout of the object to be followed.
            frame_id (int/None): The id of the frame in the frame buffer
            box_id (int/None): the id of the box in the frame defined by the frame buffer

        Raises:
            TypeError: One of the attributes given is of the wrong type.
        """
        if not isinstance(object_id, int):
            raise TypeError('Object id should be an integer')

        if frame_id is not None and not isinstance(frame_id, float):
            raise TypeError('Frame id should be a float')

        if box_id is not None and not isinstance(box_id, int):
            raise TypeError('Box id should be an integer')

        if image is not None and (not isinstance(image, str) or not image.startswith('data:image/png;base64')):
            raise TypeError('Image should be a string (base64 encoded)')

        # Set the cutout to none.
        self.__cutout = None

        self.__base_64_image = None
        # Convert the cutout (if it exist), to an openCV image, rather than a base 64 encoded image.
        if image is not None:
            self.__base_64_image = image
            self.__image = self.__convert_base64_image_to_np_array(image)
        else:
            self.__image = None

        self.__object_id = object_id
        self.__box_id = box_id
        self.__frame_id = frame_id

    @staticmethod
    def from_message(message):
        """Converts a python dict representation of the message to a StartCommand.

        Args:
            message (dict): Python dict representation of an incoming JSON message.

        Returns:
            (StartMessage): StartCommand constructed from the dict.

        Raises:
            KeyError: One or more of the expected keys needed for the start message is missing
        """
        if 'objectId' not in message.keys():
            raise KeyError('objectId missing')

        # The start command should at least contain either a cutout, or a box_id and frame_id.from.
        # Otherwise, there is not enough data to generate a cutout.
        if 'image' not in message.keys() and ('boxId' not in message.keys() or 'frameId' not in message.keys()):
            raise KeyError('Not enough data for cutout in message')

        object_id = message['objectId']

        # These could all possibly be none.
        image = message.get('image', None)
        box_id = message.get('boxId', None)
        frame_id = message.get('frameId', None)
        return StartMessage(object_id, image, frame_id, box_id)

    def to_message(self):
        """Converts the StartMessage to a dict representation.

        Returns:
            (dict): Python dict representation of the message.
        """
        message = {'type': 'start', 'objectId': self.__object_id}
        if self.__box_id:
            message['boxId'] = self.__box_id
        if self.__frame_id:
            message['frameId'] = self.__frame_id
        if self.__base_64_image is not None:
            # Encode the image back to base64.
            message['image'] = self.__base_64_image

        return message

    def get_cutout(self, framebuffer):
        """Tries to get the cutout from the information in the StartMessage.

        The cutout is retrieved either from the frame buffer if that is possible.
        Otherwise directly from the sent image if that is possible.
        Otherwise raise an error and don't follow the subject.

        Args:
            framebuffer (FrameBuffer): frame buffer object that contains the different frames.

        Returns:
            (np.ndarray): OpenCV-readable cutout of the subject to be followed.

        Raises:
            IndexError: Frame was not found in the frame buffer.
            ValueError: Box identifier was not found inside the frame stored in buffer.
        """
        # If the cutout was already found before, don't try to find it again.
        if self.__cutout is not None:
            return self.__cutout

        # Try to find the frame in the frame buffer if it was not already found before.
        error = None

        if self.__frame_id is not None and self.__box_id is not None:
            try:
                stored_frame = framebuffer.get_frame(self.__frame_id).frame
                stored_box = framebuffer.get_box(self.__frame_id, self.__box_id)
                self.__cutout = slice_bounding_box(stored_box, stored_frame)
                return self.__cutout
            # Frame could not be found in the frame buffer, it was probably too small.
            except IndexError as index_error:
                error = index_error
            # Box was not found in image.
            except ValueError as value_error:
                error = value_error

        # We can still get the data from the image.
        if self.__image is not None:
            self.__cutout = self.__image
            return self.__cutout

        # There is no way to get the image. Log this and don't use the tracking data.
        raise error

    @staticmethod
    def __convert_base64_image_to_np_array(image):
        """Converts the base64 encoded image from the websocket to a np array usable by OpenCV.

        Args:
            image (string): a string of the image in base64 png format.

        Returns:
            (np.ndarray): the image in OpenCV-readable format.
        """
        encoded_data = base64.b64decode(image.split(',')[1])
        np_rep = np.frombuffer(encoded_data, np.uint8)
        decoded_data = cv2.imdecode(np_rep, cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(decoded_data, cv2.COLOR_RGBA2RGB)

    @property
    def object_id(self):
        """Get object id.

        Returns:
            (int): Identifier of the object to stop following.
        """
        return self.__object_id

    @property
    def base64_image(self):
        """Get base64 image.

        Returns:
            (str/None): Base64 encoded image.
        """
        return self.__base_64_image

    @property
    def frame_id(self):
        """Get frame id.

        Returns:
            (float): Identifier of the frame that contains the object to be followed.
        """
        return self.__frame_id

    @property
    def box_id(self):
        """Get box id.

        Returns:
            (int): Identifier of the box that contains the object to be followed.
        """
        return self.__box_id

    def __eq__(self, other):
        """Function that checks whether the current StartCommand is the same as the given one.

        Args:
            other (StartMessage): StartCommand to compare with.

        Returns:
            (bool): Whether the messages are the same.
        """
        return all([self.__object_id == other.object_id,
                    self.__base_64_image == other.base64_image,
                    self.box_id == other.box_id,
                    self.frame_id == other.frame_id])

    def __repr__(self):
        """Converts the StartMessage to a string.

        Returns:
            (str): String representation of a StartMessage.
        """
        return f'StartMessage(object id: {self.__object_id} image: ' \
               f'{self.__base_64_image if self.__base_64_image is not None else "None"} ' \
               f'box id: {self.__box_id if self.__box_id is not None else "None"} ' \
               f'frame id: {self.__frame_id if self.frame_id is not None else "None"})'
