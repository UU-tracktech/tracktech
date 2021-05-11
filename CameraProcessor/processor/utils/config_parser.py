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
        self.root_path = os.path.join(__file__, '../../../')
        self.config_path = os.path.realpath(os.path.join(self.root_path, config_name))

        # Make sure path does indeed exist
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f'Config file does not exist in {self.root_path} + {config_name}')

        # Read config file
        self.configs = configparser.ConfigParser(allow_no_value=True)
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
