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
try:
    import RPi.GPIO as GPIO
except:
    pass
import datetime
from HAB.parsing.parser import Parser

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
        This constructor initialize the the required parameter
        """

        parser = Parser(filename=filename)
        self.uuid = parser.segregated(parser.read(),'UUID')
        self.id = parser.segregated(parser.read(),'ID')
        self.rate = parser.segregated(parser.read(),'RATE')
        self.gpio = parser.segregated(parser.read(),'GPIO')
        self.ddl = parser.segregated(parser.read(),'DATA_DELIVERY_LOCATION')

    def payload_creation(self, data):
        """
        This method create the payload
        UUID: unique identification key
        ID: device id
        RATE: rate of data pulling
        GPIO: gpio pin on which hardware is controlling
        DDL: data delivery location
        VALUE: device sensed value
        TIME: time on which device value was sensed
        :return: dictionary of payload
        """

        payload = {}
        payload['UUID'] = self.uuid
        payload['ID'] = self.id
        payload['RATE'] = self.rate
        payload['GPIO'] = self.gpio
        payload['DDL'] = self.ddl
        payload['VALUE'] = data[0]
        payload['TIME'] = data[1]

        return payload

    def scrap_data(self, device):
        """
        This method basically read the gpio state
        and prepare the data packet to send
        :return: data object contained the time and GPIO state
        """
        gpio = [i[1] for i in zip(self.id, self.gpio) if i[0] == device]
        if gpio:
            try:
                GPIO.setmode(GPIO.BCM)
                return [datetime.datetime.now(),GPIO.input(int(self.gpio))]
            except:
                return []
        else:
            return []

    def save_data(self):
        """
        :return:
        """
        pass