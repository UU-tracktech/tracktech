"""Constructs paths from config reader

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)

"""

import os
import configparser


class ConfigParser:
    """Config parser class that reads the config file, replaces all paths with the absolute one

    Attributes:
        root_path (str): path to root
        config_path (str): path to config file
        configs (configparser.ConfigParser): config parser containing keys and values
    """
    def __init__(self, config_name):
        """Creates the config and reads the values, converts paths to absolute

        Args:
            config_name (str): name of the config file
        """
        # Config path
        self.root_path = os.path.realpath(os.path.join(__file__, '../../../'))
        self.config_path = os.path.join(self.root_path, config_name)

        # Make sure path does indeed exist
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f'Config file does not exist in {self.config_path}')

        # Read config file
        self.configs = configparser.ConfigParser(allow_no_value=True, converters={'tuple': self.__parse_int_tuple})
        self.configs.read(self.config_path)

        # Converts paths
        self.__convert_paths_to_absolute()

    def __convert_paths_to_absolute(self):
        """Converts keys that end with path to absolute paths
        """
        for section in self.configs:
            for section_key in self.configs[section]:
                if section_key.endswith('path'):
                    self.configs[section][section_key] = \
                        os.path.realpath(os.path.join(self.root_path, self.configs[section][section_key]))

    def append_config(self, config_name):
        """Appends another config file to the self.configs

        Args:
            config_path (str): File name of the configuration file that needs to get appended
        """
        temp_config_path = os.path.realpath(os.path.join(self.root_path, config_name))
        temp_configs = configparser.ConfigParser(allow_no_value=True, converters={'tuple': self.__parse_int_tuple})
        temp_configs.read(temp_config_path)

        # Each section
        for section in temp_configs:
            # Make sure key exists
            if not self.configs.has_section(section):
                continue
            # If also option exists, give new value from temp_configs
            for section_key in temp_configs[section]:
                if not self.configs.has_option(section, section_key):
                    continue
                if section_key.endswith('path'):
                    self.configs[section][section_key] = \
                        os.path.realpath(os.path.join(self.root_path, temp_configs[section][section_key]))
                else:
                    self.configs[section][section_key] = temp_configs[section][section_key]

    @staticmethod
    def __parse_int_tuple(item):
        """Converter for parsing a tuple
        """
        return tuple(int(k.strip()) for k in item[1:-1].split(','))
