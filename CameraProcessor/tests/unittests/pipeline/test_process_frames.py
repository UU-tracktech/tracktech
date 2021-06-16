"""Testing files for process frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import asyncio
import pytest

from tests.unittests.utils.fake_detector import FakeDetector
from tests.unittests.utils.fake_tracker import FakeTracker
from tests.unittests.utils.fake_re_identifier import FakeReIdentifier
from tests.unittests.utils.fake_websocket import FakeWebsocket
from processor.pipeline.prepare_pipeline import prepare_objects
from processor.pipeline.process_frames import process_stream
from processor.pipeline.detection.yolov5_detector import Yolov5Detector
from processor.pipeline.detection.yolor_detector import YolorDetector
from processor.input.video_capture import VideoCapture
from processor.websocket.boxes_message import BoxesMessage


class TestProcessFrames:
    """Tests process_frames.py."""
    def __get_video(self, configs):
        """Get the video capture.

        Args:
            configs (ConfigParser): Configurations of the test.

        Returns:
            VideoCapture: A VideoCapture object streaming the source path.
        """
        __videos_dir = configs['Yolov5']['source_path']
        return VideoCapture(__videos_dir)

    def __get_yolov5runner(self, configs):
        """Get the Yolov5 runner.

        Args:
            configs (ConfigParser): Configurations of the test.

        Returns:
            Yolov5Detector: Detection object of yolov5.
        """
        return Yolov5Detector(configs['Yolov5'], configs['Filter'])

    def __get_yolorrunner(self, configs):
        """Get the YOLOR runner.

        Args:
            configs (ConfigParser): Configurations of the test.

        Returns:
            YolorDetector: Detection object of YOLOR.
        """
        return YolorDetector(configs['Yolor'], configs['Filter'])

    # pylint: disable=useless-return
    def __get_sort_tracker(self):
        """Get the SORT tracker.

        Returns:
            FakeTracker: Fake tracker implementation.
        """
        # TODO Actually return SORT maybe # pylint: disable=fixme.
        return FakeTracker()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolov5(self, configs):
        """Tests process_stream function using Yolov5.

        Note:
            I tried parametrizing Yolov5 via a fixture, but that does not work for some reason.

        Args:
            configs (ConfigParser): Configurations of the test
        """
        # Open video.
        video_capture, detector, tracker, re_identifier, _ = prepare_objects(configs)

        # Process stream and close the video.
        asyncio.get_event_loop().run_until_complete(
            self.await_detection(video_capture, detector, tracker, re_identifier))
        video_capture.close()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolor(self, configs):
        """Tests process_stream function with YOLOR.

        Note:
            Not parametrizing YOLOR for the same reason as previous function.

        Args:
            configs (ConfigParser): Configuration parser containing the configurations.
        """
        # Open video and get the runner.
        capture = self.__get_video(configs)
        unused_capture, _, tracker, re_identifier, _ = prepare_objects(configs)
        unused_capture.close()
        detector = self.__get_yolorrunner(configs)

        # Process the stream and close the capture.
        asyncio.get_event_loop().run_until_complete(self.await_detection(capture, detector, tracker, re_identifier))
        capture.close()

    @pytest.mark.timeout(90)
    def test_process_stream_with_fake(self, configs):
        """Tests process_stream with a fake detector.

        Args:
            configs (ConfigParser): Configurations of the test.
        """
        capture = self.__get_video(configs)

        # Get fake implementations.
        detector = FakeDetector()
        tracker = FakeTracker()
        re_identifier = FakeReIdentifier()

        # Process the stream and close the capture.
        asyncio.get_event_loop().run_until_complete(self.await_detection(capture, detector, tracker, re_identifier))
        capture.close()

    async def await_detection(self, capture, detector, tracker, re_identifier):
        """Async function that runs process_stream.

        Args:
            capture (ICapture): Capture implementation.
            detector (IDetector): Detection class.
            tracker (ITracker): Tracking class.
        """
        # Create fake WebSocket.
        websocket_client = FakeWebsocket()

        # Process the stream.
        await process_stream(
            capture,
            detector,
            tracker,
            re_identifier,
            lambda frame_obj, detected_boxes, tracked_boxes, re_id_tracked_boxes:
            websocket_client.send_command(BoxesMessage(frame_obj.timestamp, tracked_boxes)),
            websocket_client
        )


if __name__ == '__main__':
    pytest.main(TestProcessFrames)
