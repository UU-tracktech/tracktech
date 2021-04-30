"""Testing files for FrameBuffer

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""


import pytest

from processor.data_object.bounding_box import BoundingBox
from processor.pipeline.framebuffer import FrameBuffer


class TestFrameBuffer:
    """Class for testing Frame Buffer

    """

    def test_framebuffer(self):
        """Make a tracking object, update it a few times

        """
        class FrameWithShape:
            """A quick inline fake Frame class that has the needed property 'shape'

            """
            def __init__(self, num):
                self.frame = [num, num, num, num]
                self.shape = 1, 1, None

        framebuffer = FrameBuffer()
        track_obj = TrackingObj()
        det_obj = None

        for i in range(3):
            det_obj = DetectionObj(i, FrameWithShape(i), i)
            track_obj.update(det_obj)
            track_obj.bounding_boxes.append(BoundingBox(i, [i, i, i + 1, i + 1], "man", 0.65))
            framebuffer.add(track_obj.to_dict())

        for i in range(len(framebuffer.buffer)):
            obj = framebuffer.buffer.pop()
            assert obj["frame"].frame == [i, i, i, i]

    def test_framebuffer_cleanup(self):
        """Tests if the frame buffer cleans up nicely

        """
        framebuffer = FrameBuffer()
        for _ in range(60):
            framebuffer.add({})
        framebuffer.clean_up()
        assert len(framebuffer.buffer) < 51

    def test_framebuffer_search(self):
        """Tests the search function

        """
        framebuffer = FrameBuffer()
        for i in range(50):
            framebuffer.add({
                "frame": [i],
                "frameId": i,
                "boxes": []
            })

        # Add an occurrence of id 1 to frame 10 (reverse order)
        framebuffer.buffer[39]["boxes"].append({
            "boxId": 1,
            "rect": [0, 0, 0, 0]
        })

        # Add an occurrence of id 1 to frame 40 (reverse order)
        framebuffer.buffer[9]["boxes"].append({
            "boxId": 1,
            "rect": [3, 3, 5, 5]
        })

        bbox, framelist = framebuffer.search(10, 1)
        assert len(framelist) == 10
        assert bbox == [3, 3, 5, 5]


if __name__ == '__main__':
    pytest.main(TestFrameBuffer)
