"""Gets the root path of the CameraProcessor component and contains fixtures for the test configurations.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import pytest

from processor.utils.config_parser import ConfigParser

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def configs():
    """Configs fixture so pytest methods can use them easily.

    Returns:
        (configparser.ConfigParser): The test configurations.
    """
    return get_test_configs()


def get_test_configs():
    """Test configs for when fixture cannot be used.

    Returns:
        (configparser.ConfigParser): Which has the test-config appended to it.
    """
    config_parser = ConfigParser('configs.ini', False)
    config_parser.append_config('test-configs.ini')
    return config_parser.configs
