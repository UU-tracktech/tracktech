"""Tests StartMessage by checking properties.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import pytest
import numpy as np

from tests.conftest import root_path
from tests.unittests.conftest import get_small_frame
from processor.websocket.start_message import StartMessage
from processor.pipeline.frame_buffer import FrameBuffer
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.frame_obj import FrameObj
from processor.data_object.rectangle import Rectangle


# pylint: disable=attribute-defined-outside-init,no-member
class TestStartMessage:
    """Testing StartMessage.

    Attributes:
        data (StartMessage): Example StartMessage.
        other (StartMessage): Other StartMessage.
        object_id (int): Object identifier.
        frame_id (float): Frame identifier.
        box_id (int): Box identifier.
        base64_image (image): Base64 encoded image.
    """
    def setup_method(self):
        """Setup method."""
        self.object_id = 1
        self.frame_id = 2.  # Should be a float.
        self.box_id = 3
        # Hardcoded value for the small_frame image in data/unittets. Base64 encoding in Python does not return.
        with open(os.path.join(root_path, 'data/tests/unittests/base64_image.txt')) as file:
            self.base64_image = file.read()
        # The same result as the orchestrator would send/the method expects.
        self.data = StartMessage(self.object_id,
                                 image=self.base64_image,
                                 frame_id=self.frame_id,
                                 box_id=self.box_id)

    def test_init(self):
        """Tests init."""
        assert all([self.object_id == self.data.object_id,
                   self.frame_id == self.data.frame_id,
                   self.box_id == self.data.box_id,
                   self.base64_image == self.data.base64_image])

    def test_invalid_inite(self):
        """Tests whether an error is raised when the values in the StopMessage are invalid."""
        with pytest.raises(TypeError):
            StartMessage(1.)  # Test object id float rather than int.

        with pytest.raises(TypeError):
            StartMessage('1')  # Test object id string rather than int.

        with pytest.raises(TypeError):
            StartMessage(self.object_id, box_id=.1, frame_id=self.frame_id)  # Test box id float rather than int.

        with pytest.raises(TypeError):
            StartMessage(self.object_id, box_id='1', frame_id=self.frame_id)  # Test box id str rather than int.

        with pytest.raises(TypeError):
            StartMessage(self.object_id, box_id=self.box_id, frame_id=1)  # Test frame id int rather than float.

        with pytest.raises(TypeError):
            StartMessage(self.object_id, image='test')  # Image does not start with base64 encoding string.

    def test_eq(self):
        """Tests eq function."""
        self.other = StartMessage(self.object_id,
                                  image=self.base64_image,
                                  frame_id=self.frame_id,
                                  box_id=self.box_id)
        assert self.data == self.other

        assert self.data != StartMessage(self.object_id + 1,
                                         image=self.base64_image,
                                         frame_id=self.frame_id,
                                         box_id=self.box_id)

    def test_repr(self):
        """Tests the __repr__ function."""
        assert str(self.data).startswith('StartMessage(')

    def test_message_parsing(self):
        """Tests that a StopMessage constructed from a  message can be converted into the original message.

        This method tests both the from_message and to_message functionality of the class.
        """
        # Full message.
        dict_message = {'type': 'start',
                        'objectId': self.object_id,
                        'frameId': self.frame_id,
                        'boxId': self.box_id,
                        'image': self.base64_image}
        message = StartMessage.from_message(dict_message)
        assert message.to_message() == dict_message

        # No image specified.
        dict_message = {'type': 'start',
                        'objectId': self.object_id,
                        'frameId': self.frame_id,
                        'boxId': self.box_id}
        message = StartMessage.from_message(dict_message)
        assert message.to_message() == dict_message

        # No box_id and frame_id specified.
        dict_message = {'type': 'start',
                        'objectId': self.object_id,
                        'image': self.base64_image}
        message = StartMessage.from_message(dict_message)
        assert message.to_message() == dict_message

    def test_invalid_from_message(self):
        """Test that invalid message types raise a KeyError."""
        # Create invalid messages.
        missing_object_id_msg = {'type': 'start',
                                 'frameId': self.frame_id,
                                 'boxId': self.box_id}

        missing_frame_id_msg = {'type': 'start',
                                'objectId': self.object_id,
                                'boxId': self.box_id}

        missing_box_id_msg = {'type': 'start',
                              'objectId': self.object_id,
                              'frameId': self.frame_id}

        # Test whether from_message raises exception with invalid messages.
        with pytest.raises(KeyError):
            StartMessage.from_message(missing_object_id_msg)

        with pytest.raises(KeyError):
            StartMessage.from_message(missing_frame_id_msg)

        with pytest.raises(KeyError):
            StartMessage.from_message(missing_box_id_msg)

    def test_get_cutout_image_from_framebuffer(self):
        """Tests that the get_cutout function in the StartMessage works properly when using valid framebuffer."""
        fake_framebuffer = FrameBuffer(1)  # Fake frame buffer.
        fake_frame = FrameObj(get_small_frame(), self.frame_id)  # Fake frame that is the same frame as used for data.
        fake_rect = Rectangle(0., 0., 1., 1.)  # Fake rectangle that covers entire screen.
        fake_bounding_boxes = BoundingBoxes([BoundingBox(self.box_id, fake_rect, '', 1)])  # Fake BoundingBoxes.
        fake_framebuffer.add_frame(fake_frame, fake_bounding_boxes)   # Framebuffer stores single frame with single box.

        # Check that the cutout (which in this case, consists of the entire frame), is indeed equal to the original.
        cutout_by_message = self.data.get_cutout(fake_framebuffer)
        assert np.all(cutout_by_message == get_small_frame())

        # Run through twice to use the cache and check if the new cutout is the same as the first one.
        assert np.all(self.data.get_cutout(fake_framebuffer) == cutout_by_message)

    def test_get_cutout_image_from_message(self):
        """Tests that the get_cutout function in the StartMessage works if framebuffer does not contain frame."""
        fake_framebuffer = FrameBuffer(1)  # Fake frame buffer.

        # The frame buffer does not contain any frames, so the image should be used.
        # Check that the cutout, is indeed equal to the original.
        cutout_by_message = self.data.get_cutout(fake_framebuffer)
        assert np.all(cutout_by_message == get_small_frame())

    def test_invalid_get_cutout(self):
        """Tests that the get_cutout function raises an error when there is no image and the framebuffer is invalid."""
        fake_framebuffer = FrameBuffer(1)  # Fake frame buffer.
        message_without_image = StartMessage(self.object_id, frame_id=self.frame_id, box_id=self.box_id)

        # The frame buffer does not contain any frames, and there is no image, so this should fail.
        with pytest.raises(IndexError):
            message_without_image.get_cutout(fake_framebuffer)

        # Add a frame to the buffer, but with the wrong box id.
        fake_frame = FrameObj(get_small_frame(), self.frame_id)  # Fake frame that is the same frame as used for data.
        fake_rect = Rectangle(0., 0., 1., 1.)  # Fake rectangle that covers entire screen.
        fake_bounding_boxes = BoundingBoxes([BoundingBox(self.box_id + 1, fake_rect, '', 1)])  # Wrong BoundingBoxes.
        fake_framebuffer.add_frame(fake_frame, fake_bounding_boxes)

        with pytest.raises(ValueError):
            message_without_image.get_cutout(fake_framebuffer)


if __name__ == '__main__':
    pytest.main(TestStartMessage)
