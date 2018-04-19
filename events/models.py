from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'cities'


@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=11)
    longitude = models.CharField(max_length=11)

    def __str__(self):
        return "%s, %s, %s" % (self.name, self.latitude, self.longitude)

    class Meta(object):
        verbose_name_plural = 'locations'


@python_2_unicode_compatible
class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField()
    datetime = models.DateTimeField()
    address = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField()
    city = models.ManyToManyField('City')
    register_link = models.URLField(blank=True, null=True)
    sharing_text = models.CharField(max_length=140, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    has_interactions = models.BooleanField(default=False)
    interaction_text = models.CharField(max_length=200, blank=True, null=True)
    interaction_confirmation_text = models.CharField(max_length=200, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=True)
    is_interaction_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_cities(self):
        return "\n".join([c.name for c in self.city.all()])

    class Meta(object):
        ordering = ['-datetime']
        verbose_name_plural = 'events'


class EventParticipant(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey('participants.User')

    def save(self, *args, **kwargs):
        if self.id is None:
            existing_record = EventParticipant.objects.filter(event=self.event, participant=self.participant)
            if len(existing_record) > 0:
                # raise an IntegrityError is another possibility to handle duplicated records
                # from django.db import IntegrityError
                # message = "%s ya registrado en %s" % (self.participant.email, self.event.title)
                # raise IntegrityError("message")
                return

        return super(EventParticipant, self).save(*args, **kwargs)


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
