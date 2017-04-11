from __future__ import unicode_literals

from django.db import models


class Device(models.Model):
    device_code = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=10)

    class Meta(object):
        verbose_name_plural = 'devices'
