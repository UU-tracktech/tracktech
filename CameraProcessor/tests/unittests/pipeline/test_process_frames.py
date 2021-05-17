"""Testing files for process frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import asyncio
import pytest

from processor.main import send_orchestrator

from processor.utils.config_parser import ConfigParser
from processor.pipeline.process_frames import process_stream, prepare_stream
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.input.video_capture import VideoCapture

from tests.unittests.utils.fake_detector import FakeDetector
from tests.unittests.utils.fake_tracker import FakeTracker
from tests.unittests.utils.fake_websocket import FakeWebsocket

import processor.utils.config_parser

# Set test config to true, so it processes a shorter video
processor.utils.config_parser.USE_TEST_CONFIG = True


class TestProcessFrames:
    """Tests process_frames.py.

    """

    def __get_video(self):
        """Get the video capture.

        Returns: a VideoCapture object streaming test.mp4.

        """
        config_parser = ConfigParser('configs.ini')
        configs = config_parser.configs
        __videos_dir = configs['Yolov5']['source_path']
        return VideoCapture(__videos_dir)

    # pylint: disable=useless-return
    def __get_yolov5runner(self):
        """Get the Yolov5 runner.

        """
        config_parser = ConfigParser('configs.ini')
        configs = config_parser.configs
        return Yolov5Detector(configs['Yolov5'], configs['Filter'])

    # pylint: disable=useless-return
    def __get_sort_tracker(self):
        """Get the SORT tracker.
        """
        # TODO Actually return SORT maybe # pylint: disable=fixme
        return FakeTracker()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolov5(self):
        """Tests process_stream function using Yolov5.

        Note: I tried parametrizing Yolov5 via a fixture, but that does not work for some reason.

        """
        # Open video
        capture = self.__get_video()
        unused_capture, detector, tracker, _ = prepare_stream()
        unused_capture.close()

        asyncio.get_event_loop().run_until_complete(self.await_detection(capture, detector, tracker))
        capture.close()

    @pytest.mark.timeout(90)
    def test_process_stream_with_fake(self):
        """Tests process_stream with a fake detector.

        """
        captor = self.__get_video()
        detector = FakeDetector()

        tracker = FakeTracker()

        asyncio.get_event_loop().run_until_complete(self.await_detection(captor, detector, tracker))

    async def await_detection(self, captor, detector, tracker):
        """Async function that runs process_stream.

        """
        await process_stream(
            captor,
            detector,
            tracker,
            lambda frame_obj, tracked_boxes: send_orchestrator(
                FakeWebsocket(),
                frame_obj,
                tracked_boxes
            )
        )


if __name__ == '__main__':
    pytest.main(TestProcessFrames)
