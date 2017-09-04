"""
This module is responsible to execute task
asynchronously
Data (state) needs to be pull from external
hardware asynchronously and sends the state
data to server or cloud asynchronously
without disturbing the other task execution

This module also responsible to execute the
cmd received from vpn server for actuation of
external device
"""

import requests
import multiprocessing as mp

_author_ = 'dhimantarun19@gmail.com'


class Async:
    """
    """
    def __init__(self):
        """
        """
        pass

    def actuation_cmd_listner(self,device_id=None,state=None,localhost='127.0.0.1',port='8000'):
        """
        This method basically receive the commands from
        the views to actuate the hardware
        This module first check the current state and if
        state is different it sends request to change the
        state of hardware, if state are same, it will only
        the commands to the database
        :param device_id: external hardware ID
        :param state: new state to change
        :param localhost: IP of local server running
        :param port: Port on which the server is running
        :return: None
        """
        url = localhost+':'+port+'/device_id='+device_id+'/current_state'
        current_state = self.get_current_state(url)
        if current_state != state:
            url = localhost+':'+port+'/device_id='+device_id+'/new_state='+state
            if self.send():
                pass
            else:
                pass
        return None

    def send(self,url=None):
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False

    def get_current_state(self,url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            return None


