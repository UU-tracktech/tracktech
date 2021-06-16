"""Tests i_start_command.py.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import pytest

from processor.webhosting.start_command_simple import StartCommandSimple
from processor.webhosting.start_command_extended import StartCommandExtended
from processor.webhosting.start_command_search import StartCommandSearch


# pylint: disable=attribute-defined-outside-init
class TestStartCommands:
    """Tests the start commands."""

    def test_start_command_simple(self):
        """Asserts if the StartCommandSimple object initializes correctly."""
        start_commandsimple = StartCommandSimple(objectId=1, image=[1])
        assert start_commandsimple.objectId == 1
        assert start_commandsimple.image == [1]

    def test_start_command_extended(self):
        """Asserts if the StartCommandExtended object initializes correctly."""
        start_command_extended = StartCommandExtended(objectId=1, image=[1], frameId=1, boxId=1)
        assert start_command_extended.objectId == 1
        assert start_command_extended.image == [1]
        assert start_command_extended.frameId == 1
        assert start_command_extended.boxId == 1

    def test_start_command_search(self):
        """Asserts if the StartCommandSearch object initializes correctly."""
        start_command_search = StartCommandSearch(objectId=1, frameId=1, boxId=1)
        assert start_command_search.objectId == 1
        assert start_command_search.frameId == 1
        assert start_command_search.boxId == 1

    def test_verbose_start_command_simple(self):
        """Asserts a StartCommandSimple with invalid keys throws error."""
        with pytest.raises(KeyError):
            StartCommandSimple(objectId=1, image=[1], wrongkey=-1)

    def test_verbose_start_command_extended(self):
        """Asserts a StartCommandExtended with invalid keys throws error."""
        with pytest.raises(KeyError):
            StartCommandExtended(objectId=1, image=[1], frameId=1, boxId=1, wrongkey=-1)

    def test_verbose_start_command_search(self):
        """Asserts a h invalid keys throws error."""
        with pytest.raises(KeyError):
            StartCommandSearch(objectId=1, frameId=1, boxId=1, wrongkey=-1)

    def test_weak_start_command_simple(self):
        """Asserts a StartCommandSimple with missing keys throws error."""
        with pytest.raises(KeyError):
            StartCommandSimple()

    def test_weak_start_command_extended(self):
        """Asserts a StartCommandSimple with missing keys throws error."""
        with pytest.raises(KeyError):
            StartCommandExtended()

    def test_weak_start_command_search(self):
        """Asserts a StartCommandSimple with missing keys throws error."""
        with pytest.raises(KeyError):
            StartCommandSearch()


if __name__ == '__main__':
    pytest.main(TestStartCommands)
