import pytest

from processor.training.detection.train import main as train_main


class TestDetectionTrainMain:
    """Tests the train.py file by running it until completion

    """
    @pytest.mark.timeout(20)
    @pytest.mark.skip("Can't test because it tries to open a window and Docker hates that")
    def test_train(self):
        """Runs train.py"""
        train_main()


if __name__ == '__main__':
    pytest.main(TestDetectionTrainMain)