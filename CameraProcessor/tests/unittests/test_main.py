import pytest
import logging
import time

# from processor.main import main as processor_main # More ugly commenting
from tests.unittests.utils.exception_handler_process import EProcess


class TestProcessorMain:
    """

    """
    @pytest.mark.timeout(30)
    @pytest.mark.skip("YOLOv5 GPU Acceleration does not work yet in Docker")
    def test_run_main(self):
        # p = EProcess(target=processor_main, args=([],))
        p = EProcess(target=None)
        p.start()
        now = time.time()
        while now + 15 > time.time():
            if p.exception:
                p.join()
                logging.info("Exception raised in main.py")
                raise p.exception
        p.terminate()
        p.join()


if __name__ == '__main__':
    pytest.main(TestProcessorMain)
