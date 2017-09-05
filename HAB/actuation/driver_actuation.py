"""
This module is basically actuate the external
hardware, This module will read the configuration
file and control the GPIO pin accordingly
"""
try:
    import RPi.GPIO as GPIO
except:
    pass
import datetime
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
        This method create the payload dictionary
        :return: payload contain different information
        """
        payload = {}
        payload['UUID'] = self.uuid
        payload['ID'] = self.id
        payload['RATE'] = self.rate
        payload['GPIO'] = self.gpio
        payload['DDL'] = self.ddl
        payload['SC'] = self.state_change
        payload['TIME'] = datetime.datetime.now()
        return payload

    def intercept_cmd(self, new_state, device):
        """
        This function will change the GPIO state
        as per the http requested device from the
        gpio mapping vs id in configuration
        :return: status and new state
        """
        gpio = [i[1] for i in zip(self.id,self.gpio) if i[0] == device]
        if gpio:
            try:
                GPIO.setmode(GPIO.BCM)
                old_state = GPIO.input(int(gpio))
                if old_state != new_state:
                    GPIO.output(int(gpio),new_state)
                    self.state_change = new_state
                    return True,new_state
                else:
                    return False,old_state
            except:
                return False,'Exception occur'
        else:
            return False,'Device not found '+device

    def save_data(self,payload):
        """
        This method will be responsible for to save
        data information into the database and send
        this data to url defined in the configuration
        :return:
        """
        pass