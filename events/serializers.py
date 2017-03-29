from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = '__all__'
