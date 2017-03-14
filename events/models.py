from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    datetime = models.DateTimeField()
    address = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField()
    register_link = models.URLField(blank=True, null=True)
    share_text = models.CharField(max_length=140, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    has_interactions = models.BooleanField(default=False)
    interaction_text = models.CharField(max_length=200, blank=True, null=True)
    interaction_confirmation_text = models.CharField(max_length=200, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ['-datetime']
        verbose_name_plural = 'events'


@python_2_unicode_compatible
class Interaction(models.Model):
    text = models.CharField(max_length=100)
    event = models.ForeignKey(Event)
    votes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    class Meta(object):
        ordering = ['-pk']
        verbose_name = 'interaction item'
        verbose_name_plural = 'interaction items'
