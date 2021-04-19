"""Tests the captures opening and closing

"""
import pytest


class TestCaptures:

    @pytest.mark.timeout(3)
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        while not capture_implementation.opened():
            pass

    @pytest.mark.timeout(3)
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        capture_implementation.close()
        while capture_implementation.opened():
            pass
