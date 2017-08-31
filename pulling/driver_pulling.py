"""
This module is basically a interface for
pulling data from the external hardware
and pushing data to url defined in the
configuration file.

To create your own driver you need to
inherit this class and implements its methods

It will take care of data delivery to the
server. if fails it will local store the
data, and try to send later when the
server is accessible
"""

from parsing.parser import Parser

_author_ = 'dhimantarun19@gmail.com'


class Hadp:
    """
    This class is home automation data pulling
    This is the main class for data pulling driver
    This will take care of
    1 - payload creation
    2 - scrap data
    3 - save data
    """

    def __init__(self, filename):
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

    def scrap_data(self):
        """
        :return:
        """
        pass

    def save_data(self):
        """
        :return:
        """
        pass




