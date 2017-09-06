# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from HAB.models import Actuation, Data, Error

# Register your models here.

admin.site.register(Actuation)
admin.site.register(Data)
admin.site.register(Error)