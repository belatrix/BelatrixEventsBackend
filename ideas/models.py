from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Idea(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey('participants.User')
    event = models.ForeignKey('events.Event')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class IdeaParticipant(models.Model):
    idea = models.ForeignKey(Idea)
    user = models.ForeignKey('participants.User')

    def __str__(self):
        return self.idea.title

    class Meta(object):
        unique_together = ('idea', 'user')
        verbose_name = 'team member'
        verbose_name_plural = 'groups'


class IdeaVotes(models.Model):
    event = models.ForeignKey('events.Event')
    idea = models.ForeignKey(Idea)
    participant = models.ForeignKey('participants.User')

    class Meta(object):
        unique_together = ('idea', 'participant')
        verbose_name_plural = 'votes'


@python_2_unicode_compatible
class IdeaScoresCriteria(models.Model):
    name = models.CharField(max_length=200)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = 'Score category'
        verbose_name_plural = 'Score categories'


class IdeaScores(models.Model):
    idea = models.ForeignKey(Idea)
    jury = models.ForeignKey('participants.User')
    category = models.ForeignKey(IdeaScoresCriteria)
    value = models.PositiveIntegerField(default=0)

    class Meta(object):
        unique_together = ('idea', 'jury', 'category')
        verbose_name = 'Idea score'
        verbose_name_plural = 'Idea scores'
