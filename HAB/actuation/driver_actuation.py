"""
This module is basically actuate the external
hardware, This module will read the configuration
file and control the GPIO pin accordingly
"""
try:
    import RPi.GPIO as GPIO
except:
    pass
import socket
import requests
import datetime
from ..models import Actuation, Error
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

    def payload_creation(self, device):
        """
        This method create the payload dictionary
        :return: payload contain different information
        """
        gpio = int([i[1] for i in zip(self.id, self.gpio) if i[0] == device][0])
        payload = {
            'UUID': self.uuid,
            'ID': device,
            'RATE': self.rate,
            'GPIO': gpio,
            'DDL': self.ddl,
            'SC': self.state_change,
            'TIME': datetime.datetime.now()
        }
        return payload

    def intercept_cmd(self, new_state, device):
        """
        This function will change the GPIO state
        as per the http requested device from the
        gpio mapping vs id in configuration
        :return: status and new state
        """
        gpio = int([i[1] for i in zip(self.id,self.gpio) if i[0] == device][0])

        if gpio:

            try:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(gpio, GPIO.OUT)
                old_state = GPIO.input(gpio)

                if old_state != new_state:
                    GPIO.output(gpio, new_state)
                    self.state_change = new_state
                    return True, old_state
                else:
                    return True, old_state

            except:
                return False, 'Exception occur'

        else:
            return False, 'Device not found '+device

    def save_data(self,payload):
        """
        This method will be responsible for to save
        data information into the local database
        :return:
        """
        if isinstance(payload['SC'], int):
            obj = Actuation(
                key=payload['UUID'],
                device_id=payload['ID'],
                rate=payload['RATE'],
                gpio=payload['GPIO'],
                state_change=payload['SC'],
                date=payload['TIME']
            )
        else:
            obj = Error(
                key=payload['UUID'],
                device_id=payload['ID'],
                rate=payload['RATE'],
                gpio=payload['GPIO'],
                error=1,
                date=payload['TIME']
            )
        obj.save()

    def internet_on(self):
        """
        This method is to check,if system is connected
        to internet or not
        :return: boolean value, True or False
        """
        try:
            host = socket.gethostbyname('www.google.com')
            s = socket.create_connection((host,80),2)
            return True
        except:
            return False

    def send_data(self):
        """
        This method will send the data to DDL
        define in the configuration
        :return:
        """
        url = self.ddl
        act = Error.objects.all()
        print (act)