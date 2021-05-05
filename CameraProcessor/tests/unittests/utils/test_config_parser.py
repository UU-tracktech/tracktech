"""Tests config parser.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""
import pytest
import os
import configparser

from processor.utils.config_parser import ConfigParser

class TestConfigParser:
    """Tests whether the ConfigParsers runs correctly.

    Attributes:
        config_parser (ConfigParser): Config parser created from reading ini
        configs (configparser.ConfigParser): configs that are adapted by the config_parser
    """
    def setup_method(self):
        """Initialise before tests."""
        self.config_parser = ConfigParser('configs.ini')
        self.configs = self.config_parser.configs

    def test_not_empty(self):
        """Asserts if config is not empty."""
        assert len(self.configs) > 0

    def test_parse_paths_correct(self):
        """Asserts if paths are parsed correctly."""
        # Reading config
        config_path = os.path.realpath(os.path.join(self.config_parser.root_path, 'configs.ini'))
        configs_old = configparser.ConfigParser(allow_no_value=True)
        configs_old.read(config_path)

        # Checking if all paths contain the root path
        for section in configs_old:
            for section_key in section:
                if section_key.endswith('path'):
                    assert section_key.startswith(self.config_parser.root_path)

    def test_invalid_file_name(self):
        """Asserts if file is invalid."""
        with pytest.raises(FileNotFoundError):
            assert ConfigParser('invalidfilename')
