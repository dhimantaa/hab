# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser
from django.http import HttpResponse, JsonResponse
import HAB.actuation.driver_actuation as da
import json

obj = Parser(filename='home.ini')
driver = da.Hada('home.ini')


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

    status, old_state = driver.intercept_cmd(int(state), device)
    payload = driver.payload_creation(device)
    if status:
        driver.save_data(payload)
        return HttpResponse(
            json.dumps(
                {
                    'Status': 'Success',
                    'New state': state,
                    'Old state': old_state
                }),
            content_type='application/json'
        )
    else:
        payload['SC'] = old_state
        driver.save_data(payload)
        return HttpResponse(
            json.dumps(
                {
                    'Status': 'Failure',
                    'New state': 'Unknown',
                    'Old state': old_state
                }),
            content_type='application/json'
        )


def send(request):
    print ('Creating background task for Error values')
    da.send_data(False, repeat=10)
    print ('Creating background task for data values')
    da.send_data(True, repeat=10)
    return JsonResponse({},status=302)
