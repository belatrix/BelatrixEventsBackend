from rest_framework import serializers
from events.models import Event
from participants.models import User
from .models import Idea


class AuthorSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ('id', 'title', 'image')


class IdeaSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    event = EventSerializer()

    class Meta(object):
        model = Idea
        fields = ('id', 'author', 'title', 'description', 'event')
        depth = 1
