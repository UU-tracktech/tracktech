"""Constructs paths from config reader and reads environment variables.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import os
import configparser
import logging


class ConfigParser:
    """Config parser class that reads the config file, replaces all paths with the absolute one.

    Attributes:
        root_path (str): path to root
        config_path (str): path to config file
        configs (configparser.ConfigParser): config parser containing keys and values
    """
    def __init__(self, config_name, use_environment_vars):
        """Creates the config and reads the values, converts paths to absolute.

        Args:
            config_name (str): name of the config file.
            use_environment_vars (bool): Use environment variables

        Raises:
            FileNotFoundError: The configuration file name searched for does not exist.
        """
        # Config path.
        self.root_path = os.path.realpath(os.path.join(__file__, '../../../'))
        self.config_path = os.path.join(self.root_path, config_name)

        # Make sure path does indeed exist.
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f'Config file does not exist in {self.config_path}')

        # Read config file.
        self.configs = configparser.ConfigParser(allow_no_value=True, converters={'tuple': self.__parse_int_tuple})
        self.configs.read(self.config_path)

        # Also use environment variables in case those are needed.
        if use_environment_vars:
            logging.info('Using environment variables')
            self.read_environment_variables()

        # Converts paths.
        self.__convert_paths_to_absolute()

    def __convert_paths_to_absolute(self):
        """Converts keys that end with path to absolute paths."""
        for section in self.configs:
            for section_key in self.configs[section]:
                if section_key.endswith('path'):
                    self.configs[section][section_key] = \
                        os.path.realpath(os.path.join(self.root_path, self.configs[section][section_key]))

    def append_config(self, config_name):
        """Appends another config file to the self.configs.

        Args:
            config_name (str): File name of the configuration file that needs to get appended.
        """
        temp_config_path = os.path.realpath(os.path.join(self.root_path, config_name))
        temp_configs = configparser.ConfigParser(allow_no_value=True, converters={'tuple': self.__parse_int_tuple})
        temp_configs.read(temp_config_path)

        # Each section.
        for section in temp_configs:
            # Make sure key exists.
            if not self.configs.has_section(section):
                continue
            # If also option exists, give new value from temp_configs.
            for section_key in temp_configs[section]:
                if not self.configs.has_option(section, section_key):
                    continue
                if section_key.endswith('path'):
                    self.configs[section][section_key] = \
                        os.path.realpath(os.path.join(self.root_path, temp_configs[section][section_key]))
                else:
                    self.configs[section][section_key] = temp_configs[section][section_key]

    def read_environment_variables(self):
        """Override configurations using environment variables.

        These properties can be changed within the docker-compose file
        in order to expose more to the outside and create an easier plug-and-play environment.
        """

        # Read all the environment variables.
        orchestrator_url = os.getenv('ORCHESTRATOR_URL')
        forwarder_url = os.getenv('FORWARDER_URL')
        running_mode = os.getenv('PROCESSOR_MODE')
        detection_alg = os.getenv('DETECTION_ALG')
        tracking_alg = os.getenv('TRACKING_ALG')
        reid_alg = os.getenv('REID_ALG')

        # Replace values inside the configuration when set.
        if orchestrator_url is not None:
            logging.info('Environment variable: ORCHESTRATOR_URL used.')
            self.configs['Orchestrator']['url'] = orchestrator_url

        if forwarder_url is not None:
            logging.info('Environment variable: FORWARDER_URL used.')
            self.configs['HLS']['url'] = forwarder_url

        if running_mode is not None:
            logging.info('Environment variable: PROCESSOR_MODE used.')
            self.configs['Main']['mode'] = running_mode

        if detection_alg is not None:
            logging.info('Environment variable: DETECTION_ALG used.')
            self.configs['Main']['detector'] = detection_alg

        if tracking_alg is not None:
            logging.info('Environment variable: TRACKING_ALG used.')
            self.configs['Main']['tracker'] = tracking_alg

        if reid_alg is not None:
            logging.info('Environment variable: REID_ALG used.')
            self.configs['Main']['reid'] = reid_alg

    @staticmethod
    def __parse_int_tuple(item):
        """Converter for parsing a tuple.

        Args:
            item (int, int): Tuple that needs to get parsed.
        """
        return tuple(int(k.strip()) for k in item[1:-1].split(','))
