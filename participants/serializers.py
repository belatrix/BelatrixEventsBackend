from rest_framework import serializers
from .models import User, Role

from events.models import Event, Meeting
from ideas.models import Idea


class RoleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta(object):
        model = User
        fields = ('id',
                  'email',
                  'full_name',
                  'phone_number',
                  'role',
                  'is_moderator',
                  'is_staff',
                  'is_active',
                  'is_jury',
                  'is_password_reset_required')


class UserCreationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)


class UserProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=16, required=False)
    role_id = serializers.IntegerField(required=False)


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


class EventSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Event
        fields = ('id', 'title')


class EventProfileSerializer(serializers.Serializer):
    event = EventSerializer()


class IdeaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Idea
        fields = ('id', 'title')


class IdeaProfileSerializer(serializers.Serializer):
    idea = IdeaSerializer()


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Idea
        fields = ('id', 'title')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Meeting
        fields = ('id', 'name')


class AttendanceProfileSerializer(serializers.Serializer):
    meeting = MeetingSerializer()
