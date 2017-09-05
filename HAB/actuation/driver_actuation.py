"""
This module is basically actuate the external
hardware, This module will read the configuration
file and control the GPIO pin accordingly
"""
try:
    import RPi.GPIO as GPIO
except:
    pass
from HAB.parsing.parser import Parser

_author_ = 'dhimantarun19@gmail.com'


class Hada:
    """
    This class is home automation data actuation
    This is the main class for hardware actuation
    This will take care of
    1 - payload creation
    2 - intercept command
    3 - save the result
    """
    def __init__(self, filename):
        """
        This constructor initialize the the parameter required
        """

        parser = Parser(filename=filename)
        self.uuid = parser.segregated(parser.read(), 'UUID')
        self.id = parser.segregated(parser.read(), 'ID')
        self.rate = parser.segregated(parser.read(), 'RATE')
        self.gpio = parser.segregated(parser.read(), 'GPIO')
        self.ddl = parser.segregated(parser.read(), 'DATA_DELIVERY_LOCATION')
        self.state_change = None

    def payload_creation(self):
        """
        :return: payload contain different information
        """
        payload = {}
        payload['UUID'] = self.uuid
        payload['ID'] = self.id
        payload['RATE'] = self.rate
        payload['GPIO'] = self.gpio
        payload['DDL'] = self.ddl
        payload['SC'] = self.state_change
        return payload

    def intercept_cmd(self, new_state, device):
        """
        :return: None
        """
        combination = zip(self.id,self.gpio)
        gpio = ([i[1] for i in combination if i[0] == device])
        try:
            GPIO.setmode(GPIO.BCM)
            old_state = GPIO.input(int(gpio))
            if old_state != new_state:
                GPIO.output(int(gpio),new_state)
                self.state_change = new_state
                return True
            else:
                return False
        except:
            return False

    def save_data(self,payload):
        """
        :return:
        """
        pass