import pytest
import asyncio
import configparser
import time
import os

from processor.pipeline.process_frames import process_stream
from processor.pipeline.detection.detection_obj import DetectionObj
from processor.input.video_capture import VideoCapture
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from tests.unittests.utils.fake_detector import FakeDetector


class TestProcessFrames:
    """Tests process_frames.py

    """

    def __get_video(self):
        """Get the video capture

        Returns: a VideoCapture object streaming test.mp4

        """
        __root_dir = os.path.join(os.path.dirname(__file__), '../../../')
        # __folder_name = 'test'
        __videos_dir = os.path.realpath(os.path.join(__root_dir, 'data/videos/test.mp4'))
        return VideoCapture(__videos_dir)

    def __get_yolov5runner(self):
        """Get the Yolov5 runner

        """
        configs = configparser.ConfigParser(allow_no_value=True)
        __root_dir = os.path.join(os.path.dirname(__file__), '../../../')
        configs.read(os.path.realpath(os.path.join(__root_dir, 'configs.ini')))
        config = configs["Yolov5"]
        return Yolov5Detector(config)

    @pytest.mark.asyncio
    @pytest.mark.timeout(90)
    @pytest.mark.skip("YOLOv5 GPU acceleration does not work in Docker yet")
    def test_process_stream_with_yolov5(self, clients):
        """Tests process_stream function using Yolov5

        Note: I tried parametrizing Yolov5 via a fixture, but that does not work for some reason.

        """
        captor = self.__get_video()
        detector = self.__get_yolov5runner()

        # Create a detection object
        local_time = time.localtime()
        det_obj = DetectionObj(local_time, None, 0)

        asyncio.get_event_loop().run_until_complete(self.await_detection(captor, det_obj, detector, clients))

    @pytest.mark.timeout(90)
    def test_process_stream_with_fake(self, clients):
        """Tests process_stream with a fake detector

        """
        captor = self.__get_video()
        detector = FakeDetector()

        # create a detection object
        local_time = time.localtime()
        det_obj = DetectionObj(local_time, None, 0)

        asyncio.get_event_loop().run_until_complete(self.await_detection(captor, det_obj, detector, clients))

    async def await_detection(self, captor, det_obj, detector, ws_client):
        await process_stream(captor, det_obj, detector, ws_client)


if __name__ == '__main__':
    pytest.main(TestProcessFrames)