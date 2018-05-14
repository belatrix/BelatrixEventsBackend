from rest_framework import serializers
from .models import City, Event, Interaction, Meeting


class CitySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = City
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = '__all__'
        depth = 1


class InteractionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Interaction
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Meeting
        fields = '__all__'
