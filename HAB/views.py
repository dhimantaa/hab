# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import HAB.actuation.driver_actuation as da
import json

obj = Parser(filename='home.ini')


def index(request):
    print (obj.__doc__)
    return HttpResponse(json.dumps(obj.read()),content_type='application/json')


def actuation(request, device, states):
    driver = da.Hada('home.ini')
    pass
