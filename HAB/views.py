# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser
from django.http import HttpResponse
import HAB.actuation.driver_actuation as da
import json

obj = Parser(filename='home.ini')


def index(request):
    return HttpResponse(
        json.dumps(obj.read()),
        content_type='application/json'
    )


def actuation(request, device, state):
    """
    This method is the interface between the outside
    and the RPi GPIO control
    By this view we can control the GPIO
    :param request: http request object
    :param device: contain the device id
    :param state: contain the new state to change
    :return: json response of state change
    """
    driver = da.Hada('home.ini')
    status,change_state = driver.intercept_cmd(state,device)
    print (state,change_state)
    payload = driver.payload_creation()
    driver.save_data(payload)
    if status:
        return HttpResponse(
            json.dumps({'Status': 'Success', 'New state': change_state, 'Old state': state}),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({'Status': 'Failure', 'New state': change_state, 'Old state': state}),
            content_type='application/json'
        )