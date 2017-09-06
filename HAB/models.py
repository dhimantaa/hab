# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.


class Actuation(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    device_id = models.IntegerField()
    rate = models.IntegerField()
    gpio = models.IntegerField()
    state_change = models.IntegerField()
    date = models.DateTimeField()


class Error(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    device_id = models.IntegerField()
    rate = models.IntegerField()
    gpio = models.IntegerField()
    error = models.IntegerField()
    date = models.DateTimeField()

class Data(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    device_id = models.IntegerField()
    rate = models.IntegerField()
    state = models.IntegerField()
    date = models.DateTimeField()
