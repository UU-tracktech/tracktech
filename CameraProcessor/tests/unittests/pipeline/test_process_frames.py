"""Testing files for process frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import asyncio
import pytest

from processor.pipeline.process_frames import send_to_orchestrator

from processor.pipeline.process_frames import process_stream, prepare_stream
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.pipeline.detection.yolor_runner import YolorDetector
from processor.input.video_capture import VideoCapture

from tests.unittests.utils.fake_detector import FakeDetector
from tests.unittests.utils.fake_tracker import FakeTracker
from tests.unittests.utils.fake_websocket import FakeWebsocket


class TestProcessFrames:
    """Tests process_frames.py.

    """
    def __get_video(self, configs):
        """Get the video capture.

        Args:
            configs (ConfigParser): Configurations of the test

        Returns:
            VideoCapture: A VideoCapture object streaming the source path
        """
        __videos_dir = configs['Yolov5']['source_path']
        return VideoCapture(__videos_dir)

    def __get_yolov5runner(self, configs):
        """Get the Yolov5 runner.

        Args:
            configs (ConfigParser): Configurations of the test
        """
        return Yolov5Detector(configs['Yolov5'], configs['Filter'])

    # pylint: disable=useless-return
    def __get_yolorrunner(self, configs):
        """Get the YOLOR runner

        """
        return YolorDetector(configs['Yolor'], configs['Filter'])

    # pylint: disable=useless-return
    def __get_sort_tracker(self):
        """Get the SORT tracker.
        """
        # TODO Actually return SORT maybe # pylint: disable=fixme
        return FakeTracker()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolov5(self, configs):
        """Tests process_stream function using Yolov5.

        Note: I tried parametrizing Yolov5 via a fixture, but that does not work for some reason.

        Args:
            configs (ConfigParser): Configurations of the test
        """
        # Open video
        video_capture, detector, tracker, _, _ = prepare_stream(configs)

        asyncio.get_event_loop().run_until_complete(self.await_detection(video_capture, detector, tracker))
        video_capture.close()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolor(self, configs):
        """Tests process_stream function with YOLOR

        Note: Not parametrizing Yolor for the same reason as previous function, but this is a bunch of duplicate
        code now so that sucks.

        """
        # Open video
        capture = self.__get_video(configs)
        unused_capture, _, tracker, _, _ = prepare_stream(configs)
        unused_capture.close()
        detector = self.__get_yolorrunner(configs)

        asyncio.get_event_loop().run_until_complete(self.await_detection(capture, detector, tracker))
        capture.close()

    @pytest.mark.timeout(90)
    def test_process_stream_with_fake(self, configs):
        """Tests process_stream with a fake detector.

        Args:
            configs (ConfigParser): Configurations of the test
        """
        capture = self.__get_video(configs)
        detector = FakeDetector()

        tracker = FakeTracker()

        asyncio.get_event_loop().run_until_complete(self.await_detection(capture, detector, tracker))
        capture.close()

    async def await_detection(self, captor, detector, tracker):
        """Async function that runs process_stream.

        """
        websocket_client = FakeWebsocket()
        await process_stream(
            captor,
            detector,
            tracker,
            lambda frame_obj, detected_boxes, tracked_boxes: send_to_orchestrator(
                websocket_client,
                frame_obj,
                detected_boxes,
                tracked_boxes
            ),
            websocket_client
        )


if __name__ == '__main__':
    pytest.main(TestProcessFrames)
