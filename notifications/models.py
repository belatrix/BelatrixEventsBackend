from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Message(models.Model):
    text = models.CharField(max_length=140)
    event = models.ForeignKey('events.Event')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    class Meta(object):
        verbose_name_plural = 'messages'
