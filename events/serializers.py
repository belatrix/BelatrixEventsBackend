from rest_framework import serializers
from .models import Event, Interaction


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = '__all__'
        depth = 1


class InteractionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Interaction
        fields = '__all__'
