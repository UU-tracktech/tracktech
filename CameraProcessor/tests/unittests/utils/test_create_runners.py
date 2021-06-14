"""Tests the create_runners in processor.utils.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

# For use of fixtures import is needed.
import pytest  # pylint: disable=unused-import

from processor.utils.create_runners import DETECTOR_SWITCH, TRACKER_SWITCH, create_detector, create_tracker


class TestCreateRunners:
    """Class holding test functions for create_runners.py."""
    def test_create_detector(self, configs):
        """Tests the create_detector with every detector in the DETECTOR_SWITCH.

        Args:
            configs (dict): the configs file with test configs appended
        """
        for key, value in DETECTOR_SWITCH.items():
            detector = create_detector(key, configs)
            assert isinstance(detector, value[0])

    def test_create_tracker(self, configs):
        """Tests the create_tracker with every tracker in the TRACKER_SWITCH.

        Args:
            configs (dict): the configs file with test configs appended
        """
        for key, value in TRACKER_SWITCH.items():
            tracker = create_tracker(key, configs)
            assert isinstance(tracker, value[0])
