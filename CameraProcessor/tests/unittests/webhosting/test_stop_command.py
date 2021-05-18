"""Tests stop_command.py

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest

from processor.webhosting.stop_command import StopCommand


# pylint: disable=attribute-defined-outside-init
class TestStopCommand:
    """Tests the stop command."""

    def setup_method(self):
        """Creates a StopCommand object"""
        self.start = StopCommand(1)

    def test_stop_command(self):
        """Asserts if StopCommand object has been initialized correctly."""
        assert self.start.object_id == 1


if __name__ == '__main__':
    pytest.main(TestStopCommand)
