from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = '__all__'
