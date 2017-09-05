"""
This module will find the configuration .ini file
parse the configuration written inside for further
actuation and data pulling from the external hardware
"""

import os
from configobj import ConfigObj
from django.conf import settings

_author_ = 'dhimantarun19@gmail.com'


class Parser:
    """
    This class is responsible to parse the configuration
    of attached hardware and
    defines in configuration/
    """

    def __init__(self, filename=None):
        """
        Initialize the configuration file path
        """

        self.config_path = os.path.join(settings.BASE_DIR, 'HAB/configuration/' + filename)

    def read(self):
        """
        This function will read the configuration file and
        convert it into configobj dictionary
        :return: configobj dictionary of config file
        """

        return ConfigObj(self.config_path)

    def segregated(self, config, tag):
        """
        This function will segregate the information on
        the basis of tag provided by the program
        :param config:
        :param tag:
        :return: the value of tag received
        """
        for key in config.keys():
            if key == tag:
                return config[key]
            elif isinstance(config[key], dict):
                for key_one in config[key].keys():
                    if key_one == tag:
                        return config[key][key_one]
