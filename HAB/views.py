# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser
from django.http import HttpResponse
import HAB.actuation.driver_actuation as da
import json

obj = Parser(filename='home.ini')


def index(request):
    print (obj.__doc__)
    return HttpResponse(json.dumps(obj.read()),content_type='application/json')


def actuation(request, device, state):
    driver = da.Hada('home.ini')
    status = driver.intercept_cmd(state,device)
    payload = driver.payload_creation()
    driver.save_data(payload)
    if status:
        return HttpResponse(json.dumps({'Status': 'Success','New state': state}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'Status': 'Failure','New state': 'Unknown'}), content_type='application/json')