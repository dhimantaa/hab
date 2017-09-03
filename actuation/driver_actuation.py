"""
This module is basically actuate the external
hardware, This module will read the configuration
file and control the GPIO pin accordingly
"""

from parsing.parser import Parser

_author_ = 'dhimantarun19@gmail.com'


class Hada:
    """
    This class is home automation data actuation
    This is the main class for hardware actuation
    This will take care of
    1 - payload creation
    2 - intercept command
    3 - actuate gpio
    4 - save the result
    """
    def __init__(self,filename):
        """
        This constructor initialize the the parameter required
        """

        parser = Parser(filename=filename)
        self.uuid = parser.segregated(parser.read(),'UUID')
        self.id = parser.segregated(parser.read(),'ID')
        self.rate = parser.segregated(parser.read(),'RATE')
        self.gpio = parser.segregated(parser.read(),'GPIO')
        self.ddl = parser.segregated(parser.read(),'DATA_DELIVERY_LOCATION')

    def payload_creation(self):
        """
        :return:
        """
        pass

    def intercept_cmd(self):
        """
        :return:
        """
        pass

    def actuate_gpio(self):
        """
        :return:
        """
        pass

    def save_data(self):
        """
        :return:
        """
        pass