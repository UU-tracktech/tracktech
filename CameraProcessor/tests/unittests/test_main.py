"""Test main file inside unittest

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import logging
import time
import pytest

from tests.unittests.utils.exception_handler_process import EProcess


class TestProcessorMain:
    """Test main file

    """
    @pytest.mark.timeout(30)
    @pytest.mark.skip("YOLOv5 GPU Acceleration does not work yet in Docker")
    def test_run_main(self):
        """Runs the main in processor folder

        """
        process = EProcess(target=None)
        process.start()
        now = time.time()
        while now + 15 > time.time():
            if process.exception:
                process.join()
                logging.info("Exception raised in main.py")
                raise process.exception
        process.terminate()
        process.join()


if __name__ == '__main__':
    pytest.main(TestProcessorMain)
