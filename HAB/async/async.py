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

from multiprocessing import process
from functools import wraps

_author_ = 'dhimantarun19@gmail.com'


class Async:
    """
    This class is responsible to run any function
    as asynchronously
    """
    def __init__(self):
        """
        """
        pass

    def async_run(self,func):
        """
        :param func: any function to run asynchronously
        :return: return the wrapped function
        """
        @wraps(func)
        def async(*args, **kwargs):
            func_hl = process(target=func, args=args, kwargs=kwargs)
            func_hl.start()
            return func_hl

        return async

if __name__ == '__main__':
    async = Async()
    ha = Hada('home.ini')

    @async.async_run
    def run_error():
        print ('Running for error')
        ha.send_data(False)

    @async.async_run
    def run_data():
        print ('Running for data')
        ha.send_data(True)

    pass