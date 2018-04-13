from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('pk',
                  'email',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'is_participant')
