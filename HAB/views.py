# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser
from django.http import HttpResponse, JsonResponse
import HAB.actuation.driver_actuation as da
import HAB.pulling.driver_pulling as dp
import json

obj = Parser(filename='home.ini')
driver = da.Hada('home.ini')
pdriver = dp.Hadp('home.ini')


def index(request):
    return HttpResponse(
        json.dumps(obj.read()),
        content_type='application/json'
    )


def pulling(request):
    """
    This method basically start the data pulling
    from GPIO (or the Load status)
    This method will scrap the GPIO status
    and call the save function inside the driver
    to save the data to local database
    :param request: http request object
    :return: json response of process initiation
    """
    data = pdriver.scrap_data()
    for id in data:
        payload = pdriver.payload_creation(id, data[id])
        pdriver.save_data(payload)

    return HttpResponse(
        json.dumps(
            {
                'Status': 'Success',
                'Remarks': 'Data saved to local'
            }),
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
    da.send_data(False, driver.ddl, repeat=int(driver.rate))
    print ('Creating background task for Actuation data values')
    da.send_data(True, driver.ddl, repeat=int(driver.rate))
    print ('Creating background task for Pulling data values')
    dp.send_data(pdriver.ddl, repeat=int(pdriver.rate))
    return JsonResponse({},status=302)

