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
                  'is_password_reset_required')


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserAuthenticationResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()
    email = serializers.CharField(max_length=100)
    is_staff = serializers.BooleanField()
    is_jury = serializers.BooleanField()
    is_password_reset_required = serializers.BooleanField()


class UserUpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)
