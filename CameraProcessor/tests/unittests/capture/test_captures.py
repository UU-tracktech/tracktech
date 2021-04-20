"""Tests the captures

"""
import pytest


class TestCaptures:
    """Tests the captures opening and closing

    """
    @pytest.mark.timeout(10)
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        while not capture_implementation.opened():
            pass

    @pytest.mark.timeout(10)
    def test_next_frame(self, capture_implementation):
        """Asserts that you can get the next frame of the capture implementation

            Args:
                capture_implementation: see capture_implementation.

        """
        assert capture_implementation.get_next_frame()[0]

    @pytest.mark.timeout(60)
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        capture_implementation.close()
        while capture_implementation.opened():
            pass
