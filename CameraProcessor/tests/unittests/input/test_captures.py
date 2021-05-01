"""Tests the captures

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest


class TestCaptures:
    """Tests the captures opening and closing

    """

    def teardown_method(self):
        """Ensures proper closure of capture_implementation, even when test fails.."""
        self.capture_implementation.close()

    @pytest.mark.timeout(10)
    def test_initial_opened(self, capture_implementation):
        """Asserts capture to be opened after initialisation.

        Args:
            capture_implementation: see capture_implementation.

        """
        self.capture_implementation = capture_implementation
        while not self.capture_implementation.opened():
            pass

    @pytest.mark.timeout(10)
    def test_next_frame(self, capture_implementation):
        """Asserts that you can get the next frame of the capture implementation

            Args:
                capture_implementation: see capture_implementation.

        """
        self.capture_implementation = capture_implementation
        assert self.capture_implementation.get_next_frame()

    @pytest.mark.timeout(10)
    def test_closed(self, capture_implementation):
        """Asserts capture to not be opened after calling closed.

        Args:
            capture_implementation: see capture_implementation.

        """
        self.capture_implementation = capture_implementation
        self.capture_implementation.close()
        while self.capture_implementation.opened():
            pass
