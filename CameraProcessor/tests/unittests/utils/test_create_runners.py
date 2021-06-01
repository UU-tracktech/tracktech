"""Tests the create_runners in processor.utils

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import pytest

from processor.utils.config_parser import ConfigParser
from processor.utils.create_runners import DETECTOR_SWITCH, TRACKER_SWITCH, create_detector, create_tracker


class TestCreateRunners:
    """Class holding test functions for create_runners.py

    """
    def setup_class(self):
        """Setup for tests on class level

        """
        self.config_parser = ConfigParser('configs.ini')
        self.config_parser.append_config('test-configs.ini')

    def test_create_detector(self):
        """Tests the create_detector with every detector in DETECTOR_SWITCH

        """
        for key, value in DETECTOR_SWITCH.items():
            detector = create_detector(key, self.config_parser.configs)
            assert isinstance(detector, value[0])

    def test_create_tracker(self):
        """Tests the create_tracker with every tracker in TRACKER_SWITCH

        """
        for key, value in TRACKER_SWITCH.items():
            tracker = create_tracker(key, self.config_parser.configs)
            assert isinstance(tracker, value[0])
