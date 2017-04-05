from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Employee(models.Model):
    name = models.CharField(max_length=250)
    avatar = models.URLField(blank=True, null=True)
    email = models.EmailField()
    role = models.TextField()
    twitter = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['name']
        verbose_name_plural = 'employees'
