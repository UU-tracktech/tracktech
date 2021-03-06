"""Tests config parser.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import os
import configparser
import pytest

from tests.conftest import get_test_configs, root_path
from processor.utils.config_parser import ConfigParser


# pylint: disable=attribute-defined-outside-init
class TestConfigParser:
    """Tests whether the ConfigParsers runs correctly.

    Attributes:
        config_parser (ConfigParser): Config parser created from reading ini
        configs (configparser.ConfigParser): configs that are adapted by the config_parser
        dummy_environment_variables (dict[str, str]): Dummy environment variables for the test.
    """
    def setup_method(self):
        """Initialise before tests."""
        self.test_configs = get_test_configs()

        self.config_parser = ConfigParser('configs.ini', False)
        self.configs = self.config_parser.configs

    def test_not_empty(self):
        """Asserts if config is not empty."""
        assert len(self.configs) > 0

    def test_parse_paths_correct(self):
        """Asserts if paths are parsed correctly."""
        # Reading config.
        config_path = os.path.realpath(os.path.join(self.config_parser.root_path, 'configs.ini'))
        configs_old = configparser.ConfigParser(allow_no_value=True)
        configs_old.read(config_path)

        # Checking if all paths contain the root path.
        for section in configs_old:
            for section_key in section:
                if section_key.endswith('path'):
                    assert section_key.startswith(self.config_parser.root_path)

    def test_append_correct(self):
        """Assert if append was correct."""
        # Reading old config.
        test_config_path = os.path.realpath(os.path.join(self.config_parser.root_path, 'test-configs.ini'))
        test_configs_old = configparser.ConfigParser(allow_no_value=True)
        test_configs_old.read(test_config_path)

        # Loop over every section key pair in the config and check if the keys match.
        for section in self.test_configs:
            if not test_configs_old.has_section(section):
                continue
            for section_key in self.test_configs[section]:
                if not test_configs_old.has_option(section, section_key):
                    continue

                # Assert that the key is appended correctly.
                if section_key.endswith('path'):
                    assert self.test_configs[section][section_key].startswith(root_path)
                else:
                    assert self.test_configs[section][section_key] == test_configs_old[section][section_key]

    def test_append_fake_sections(self):
        """Configs get appended correctly and fake sections get ignored."""
        # Append configs.
        path_to_configs = os.path.join('data', 'tests', 'unittests', 'sample-test-configs.ini')
        self.config_parser.append_config(path_to_configs)

        # Fake sections do not get appended.
        assert not self.configs.has_section('Dummy')
        assert not self.configs.has_option('HLS', 'dummy')
        assert not self.configs.has_option('Yolov5', 'dummy_path')

    def test_append_existing_options(self):
        """Appending of configurations changes the options correctly."""
        # Append configs.
        path_to_configs = os.path.join('data', 'tests', 'unittests', 'sample-test-configs.ini')
        self.config_parser.append_config(path_to_configs)

        # Hls url is overwritten correctly.
        assert self.configs.has_option('Input', 'hls_url')
        assert self.configs['Input']['hls_url'] == 'http://localhost:300'

        # Root gets added to path variable.
        assert len(self.configs['Yolov5']['source_path']) > len('./data/videos/short_venice.mp4')
        assert self.configs['Yolov5']['source_path'] == \
               os.path.realpath(os.path.join(root_path, './data/videos/short_venice.mp4'))

    def test_invalid_file_name(self):
        """Asserts if file is invalid."""
        with pytest.raises(FileNotFoundError):
            assert ConfigParser('invalidfilename', False)

    def test_environment_variables(self):
        """Test whether the environment variables are correctly used."""
        # Set environment variables and init configparser.
        env_vars_dict = self.dummy_environment_variables
        self.set_environment_variables(env_vars_dict)
        config_parser = ConfigParser('configs.ini', True)
        configs = config_parser.configs

        # Assert properties are correctly set in configs.
        assert configs['Orchestrator']['url'] == env_vars_dict['ORCHESTRATOR_URL']
        assert configs['Input']['hls_url'] == env_vars_dict['HLS_STREAM_URL']
        assert configs['Main']['mode'] == env_vars_dict['PROCESSOR_MODE']
        assert configs['Main']['detector'] == env_vars_dict['DETECTION_ALG']
        assert configs['Main']['tracker'] == env_vars_dict['TRACKING_ALG']
        assert configs['Main']['reid'] == env_vars_dict['REID_ALG']

        # Remove environment variables.
        self.remove_environment_variables(self.dummy_environment_variables)

    @staticmethod
    def set_environment_variables(dict_environment_vars):
        """Set the environment variables to some test values.

        Args:
            dict_environment_vars (dict[str, str]): environment variables to set.
        """
        for key in dict_environment_vars:
            os.environ[key] = dict_environment_vars[key]

    @staticmethod
    def remove_environment_variables(dict_environment_vars):
        """Remove the environment variables again.

        Args:
            dict_environment_vars (dict[str, str]): environment variables to remove.
        """
        for key in dict_environment_vars:
            os.environ.pop(key)

    @property
    def dummy_environment_variables(self):
        """Dummy environment variables to test with.

        Returns:
            dict[str, str]: Dictionary containing example environment variables.
        """
        return {
            'ORCHESTRATOR_URL': 'test_orch_url',
            'HLS_STREAM_URL': 'test_hls_url',
            'PROCESSOR_MODE': 'test_mode',
            'DETECTION_ALG': 'test_det_alg',
            'TRACKING_ALG': 'test_track_alg',
            'REID_ALG': 'test_reid_alg'
        }
