from rest_framework import serializers
from events.models import Event
from participants.models import User

from .models import Idea, IdeaParticipant


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ('id', 'title', 'image')


class IdeaCreationSerializer(serializers.Serializer):
    author = serializers.IntegerField()
    event = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(required=False)


class IdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    event = EventSerializer()

    class Meta(object):
        model = Idea
        fields = ('id', 'author', 'title', 'description', 'event')
        depth = 1


class IdeaParticipantsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta(object):
        model = IdeaParticipant
        fields = ('user', )


class IdeaRegistrationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
