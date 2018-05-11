from rest_framework import serializers
from events.models import Event
from participants.models import User
from participants.serializers import RoleSerializer

from .models import Idea, IdeaCandidate, IdeaParticipant, IdeaScores, IdeaScoresCriteria


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta(object):
        model = User
        fields = ('id', 'full_name', 'email', 'phone_number', 'role')


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
        fields = ('id', 'author', 'title', 'description', 'event', 'is_completed', 'is_valid')
        depth = 1


class SimpleIdeaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Idea
        fields = ('id', 'title')


class IdeaParticipantsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta(object):
        model = IdeaParticipant
        fields = ('user', )


class IdeaCandidatesSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta(object):
        model = IdeaCandidate
        fields = ('user', )


class IdeaCandidateRegistrationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class IdeaRegistrationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class IdeaVoteSerializer(serializers.Serializer):
    idea_id = serializers.IntegerField()


class IdeaUpdateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)


class IdeaSerializerWithVotes(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    votes = serializers.IntegerField()


class IdeaScoresCriteriaSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = IdeaScoresCriteria
        fields = '__all__'


class IdeaScoreModelSerializer(serializers.ModelSerializer):
    jury = UserSerializer()
    idea = SimpleIdeaSerializer()
    category = IdeaScoresCriteriaSerializer()

    class Meta(object):
        model = IdeaScores
        depth = 1
        fields = ('id', 'idea', 'jury', 'category', 'value')


class IdeaScoreSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    value = serializers.IntegerField()
