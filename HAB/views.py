# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsing.parser import Parser

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json


def index(request):
    obj = Parser(filename='home.ini')
    print (obj.__doc__)
    return HttpResponse(json.dumps(obj.read()),content_type='application/json')


def async(request):
    pass
