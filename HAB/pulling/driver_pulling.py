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
import json
import datetime
import requests
from ..models import Data
from background_task import background
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

    def payload_creation(self, id, data):
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

        payload = {
            'UUID': self.uuid,
            'ID': id,
            'RATE': self.rate,
            'GPIO': data[2],
            'DDL': self.ddl,
            'VALUE': data[1],
            'TIME': data[0]
        }
        return payload

    def scrap_data(self, device):
        """
        This method basically read the gpio state
        and prepare the data packet to send
        :return: data object contained the time and GPIO state
        """
        data = {}
        for i in zip(self.id, self.gpio):
            try:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(int(i[1]), GPIO.OUT)
                data[i[0]] = [datetime.datetime.now(), GPIO.input(int(i[1])), i[1]]
            except:
                data[i[0]] = [datetime.datetime.now(), None, i[1]]

        return data

    def save_data(self, payload):
        """
        This method will be responsible for to save
        data information into the local database
        :param payload:
        :return:
        """
        obj = Data(
            key=payload['UUID'],
            device_id=payload['ID'],
            rate=payload['RATE'],
            state=payload['VALUE'],
            date=payload['TIME']
        )
        obj.save()


@background(schedule=120)
def send_data(ddl):
    """
    This method will send the data to DDL
    define in the configuration
    :return:
    """
    print (ddl)
    err = Data.objects.all().order_by('date')
    print ('Error ', err)
    for value in err:
        status_code = do_post(value, ddl, type)
        if status_code:
            Data.objects.filter(date=value.date).delete()
            print ('Delete row ', value.date)
        else:
            return False


def do_post(data, ddl):
    """
    This method will send the pulling data
    to server url defined inside the configuration
    file.
    :param data: Pulling data, device status
    :param ddl: data delivery location
    :return: Boolean values on the basis of podt request status
    """
    print (ddl)
    data = {
        'KEY': str(data.key),
        'ID': data.device_id,
        'RATE': data.rate,
        'VALUE': data.state,
        'DATE': str(data.date)
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(ddl, data=json.dumps(data),headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False