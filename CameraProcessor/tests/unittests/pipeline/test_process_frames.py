"""Testing files for process frames.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import asyncio
import pytest

from processor.utils.config_parser import ConfigParser
from processor.pipeline.process_frames import process_stream
from processor.pipeline.detection.yolov5_runner import Yolov5Detector
from processor.input.video_capture import VideoCapture
from tests.unittests.utils.fake_detector import FakeDetector
from tests.unittests.utils.fake_tracker import FakeTracker


class TestProcessFrames:
    """Tests process_frames.py.

    """

    def __get_video(self):
        """Get the video capture.

        Returns: a VideoCapture object streaming test.mp4.

        """
        config_parser = ConfigParser('configs.ini')
        configs = config_parser.configs
        __videos_dir = configs['Yolov5']['test_path']
        return VideoCapture(__videos_dir)

    # pylint: disable=useless-return
    def __get_yolov5runner(self):
        """Get the Yolov5 runner.

        """
        configs = configparser.ConfigParser(allow_no_value=True)
        configs.read(os.path.realpath(os.path.join(root_path, 'configs.ini')))
        config = configs['Yolov5']
        filters = {"targets": os.path.join(root_path, 'filter.names')}
        return Yolov5Detector(config, filters)  # ugly commenting to limit the import time in docker

    # pylint: disable=useless-return
    def __get_sort_tracker(self):
        """Get the SORT tracker.
        """
        # TODO Actually return SORT maybe # pylint: disable=fixme
        return FakeTracker()

    @pytest.mark.timeout(90)
    def test_process_stream_with_yolov5(self, clients):
        """Tests process_stream function using Yolov5.

        Note: I tried parametrizing Yolov5 via a fixture, but that does not work for some reason.

        """
        captor = self.__get_video()
        # detector = self.__get_yolov5runner()
        tracker = self.__get_sort_tracker()

        asyncio.get_event_loop().run_until_complete(self.await_detection(captor, detector, tracker, clients))

    @pytest.mark.timeout(90)
    def test_process_stream_with_fake(self, clients):
        """Tests process_stream with a fake detector.

        """
        captor = self.__get_video()
        detector = FakeDetector()

        tracker = FakeTracker()

        asyncio.get_event_loop().run_until_complete(self.await_detection(captor, detector, tracker, clients))

    async def await_detection(self, captor, detector, tracker, ws_client):
        """Async function that runs process_stream.

        """
        await process_stream(captor, detector, tracker, ws_client)


if __name__ == '__main__':
    pytest.main(TestProcessFrames)
