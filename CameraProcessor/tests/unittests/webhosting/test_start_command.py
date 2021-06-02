"""Tests start_command.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.webhosting.start_command import StartCommand


# pylint: disable=attribute-defined-outside-init
class TestStartCommand:
    """Tests the start command."""

    def setup_method(self):
        """Creates a StartCommand object."""
        self.start = StartCommand(object_id=1, frame_id=2, box_id=3)

    def test_start_command(self):
        """Asserts if StartCommand object has been initialized correctly."""
        assert self.start.object_id == 1
        assert self.start.frame_id == 2
        assert self.start.box_id == 3


if __name__ == '__main__':
    pytest.main(TestStartCommand)
