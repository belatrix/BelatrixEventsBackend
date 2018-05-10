# encoding: utf-8
from django.shortcuts import get_object_or_404, get_list_or_404
from constance import config
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from events.models import Event
from participants.models import User
from participants.permissions import IsJury, IsModerator

from .models import Idea, IdeaParticipant, IdeaVotes, IdeaScores, IdeaScoresCriteria
from .serializers import IdeaCreationSerializer, IdeaSerializer, IdeaParticipantsSerializer
from .serializers import IdeaRegistrationSerializer, IdeaVoteSerializer, IdeaSerializerWithVotes
from .serializers import IdeaUpdateSerializer, IdeaScoreSerializer, IdeaScoreModelSerializer
from .serializers import IdeaScoresCriteriaSerializer


@api_view(['DELETE', 'GET', 'PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def idea(request, idea_id):
    """
    Endpoint for get, update and delete an idea.
    ---
    GET:
        serializer: ideas.serializers.IdeaSerializer
    PATCH:
        serializer: ideas.serializers.IdeaUpdateSerializer
    """
    user = request.user
    idea = get_object_or_404(Idea, pk=idea_id)
    if request.method == 'GET':
        idea = get_object_or_404(Idea, pk=idea_id)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if user == idea.author:
        if request.method == 'DELETE':
            idea.delete()
            content = {'detail': 'Idea eliminada.'}
            return Response(content, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = IdeaUpdateSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                idea.title = serializer.validated_data['title']
                idea.description = serializer.validated_data['description']
                idea.save()
        idea = get_object_or_404(Idea, pk=idea_id)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise NotAcceptable('No puedes editar o borrar esta idea')


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def idea_create(request):
    """
    Endpoint to create ideas
    ---
    POST:
        serializer: ideas.serializers.IdeaCreationSerializer
        response_serializer: ideas.serializers.IdeaSerializer
    """
    if request.method == 'POST':
        serializer = IdeaCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            author = get_object_or_404(User, pk=serializer.validated_data['author'])
            event = get_object_or_404(Event, pk=serializer.validated_data['event'])
            title = serializer.validated_data['title']
            try:
                description = serializer.validated_data['description']
            except:
                description = None
            try:
                new_idea = Idea.objects.create(author=author, event=event, title=title, description=description)
            except Exception as e:
                print(e)
                raise NotAcceptable('Esta idea ya existe.')
            serializer = IdeaSerializer(new_idea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def idea_participants(request, idea_id):
    """
    Endpoint to get participant list group by idea
    ---
    GET:
        serializer: ideas.serializers.IdeaParticipantsSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    participants = IdeaParticipant.objects.filter(idea=idea)
    if len(IdeaParticipant.objects.filter(idea=idea, user=request.user)) > 0:
        is_registered = True
    else:
        is_registered = False
    serializer = IdeaParticipantsSerializer(participants, many=True)
    return Response({"is_registered": is_registered,
                     "team_members": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def idea_register(request, idea_id):
    """
    Endpoint to register user into an idea
    ---
    POST:
        serializer: ideas.serializers.IdeaRegistrationSerializer
    """
    serializer = IdeaRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        idea = get_object_or_404(Idea, pk=idea_id)
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])

        previous_records = IdeaParticipant.objects.filter(user=user)
        if len(previous_records) > 0:
            for record in previous_records:
                if record.idea.event == idea.event:
                    raise NotAcceptable('Ya se registro en una idea para este evento.')

        number_participants = IdeaParticipant.objects.filter(idea=idea).count()
        if config.TEAM_MAX_SIZE > number_participants and idea.is_completed is False:
            try:
                IdeaParticipant.objects.create(idea=idea, user=user)
                if IdeaParticipant.objects.filter(idea=idea).count() == config.TEAM_MAX_SIZE:
                    idea.is_completed = True
                    idea.save()
            except Exception as e:
                print(e)
                raise NotAcceptable('Ya registrado.')
        else:
            raise ValidationError(
                {'detail': 'Se alcanzó el número máximo de participantes por idea o ya está completo.'})
        participants = IdeaParticipant.objects.filter(idea=idea)
        serializer = IdeaParticipantsSerializer(participants, many=True)
        return Response({"is_registered": True,
                         "team_members": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def idea_unregister(request, idea_id):
    """
    Endpoint to register user into an idea
    ---
    POST:
        serializer: ideas.serializers.IdeaRegistrationSerializer
    """
    serializer = IdeaRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        idea = get_object_or_404(Idea, pk=idea_id)
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])
        get_object_or_404(IdeaParticipant, idea=idea, user=user).delete()
        if IdeaParticipant.objects.filter(idea=idea).count() < config.TEAM_MIN_SIZE:
            idea.is_completed = False
            idea.save()
        participants = IdeaParticipant.objects.filter(idea=idea)
        serializer = IdeaParticipantsSerializer(participants, many=True)
        return Response({"is_registered": False,
                         "team_members": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def idea_open(request, idea_id):
    """
    Endpoint to set an idea as open and allow more registrants.
    ---
    PATCH:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    user = request.user
    if idea.author == user:
        if IdeaParticipant.objects.filter(idea=idea).count() < config.TEAM_MAX_SIZE:
            idea.is_completed = False
            idea.save()
        else:
            raise ValidationError({'detail': 'Número máximo de integrantes alcanzado.'})
    else:
        raise ValidationError({'detail': 'No tienes permiso para marcar como abierto.'})
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def idea_completed(request, idea_id):
    """
    Endpoint to set an idea as completed, no more registrants allowed.
    ---
    PATCH:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    user = request.user
    if idea.author == user:
        if IdeaParticipant.objects.filter(idea=idea).count() >= config.TEAM_MIN_SIZE:
            idea.is_completed = True
            idea.save()
        else:
            raise ValidationError({'detail': 'No tienes el número mínimo de integrantes.'})
    else:
        raise ValidationError({'detail': 'No tienes permiso para marcar como completado.'})
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def idea_list(request, event_id):
    """
    Returns idea list by event
    ---
    GET:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    ideas = get_list_or_404(Idea, event=event_id, is_valid=True)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsModerator, ))
def idea_draft_list(request, event_id):
    """
    Returns idea list by event without filter
    ---
    GET:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    ideas = get_list_or_404(Idea, event=event_id)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def my_ideas(request):
    """
    Returns user idea list, not validation required and is not public.
    ---
    GET:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    ideas = Idea.objects.filter(author=request.user)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def idea_vote(request, event_id):
    """
    Endpoint to vote for an idea
    ---
    POST:
        serializer: ideas.serializers.IdeaVoteSerializer
    """
    if request.method == "POST":
        serializer = IdeaVoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            idea = get_object_or_404(Idea, pk=serializer.validated_data['idea_id'])
            user = request.user
            event = get_object_or_404(Event, pk=event_id)
            try:
                IdeaVotes.objects.create(event=event, idea=idea, participant=user)
            except Exception as e:
                print(e)
                raise NotAcceptable('Usuario ya voto')
    event_ideas = []
    ideas = get_list_or_404(Idea, event=event_id, is_valid=True)
    for idea in ideas:
        votes = IdeaVotes.objects.filter(idea=idea).count()
        idea_response = {'id': idea.id,
                         'title': idea.title,
                         'votes': votes}
        event_ideas.append(idea_response)
    serializer = IdeaSerializerWithVotes(event_ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
@permission_classes((IsModerator, ))
def idea_validate(request, idea_id):
    """
    Mark idea as valid or invalid
    ---
    PATCH:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    if idea.is_valid:
        idea.is_valid = False
    else:
        idea.is_valid = True
    idea.save()
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, IsJury))
def idea_scores_criteria(request):
    """
    Endpoint to get a list of assessment criteria for jury
    ---
    GET:
        response_serializer: ideas.serializers.IdeaScoresCriteriaSerializer
    """
    score_criteria_list = IdeaScoresCriteria.objects.all()
    serializer = IdeaScoresCriteriaSerializer(score_criteria_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH', 'POST'])
@permission_classes((IsAuthenticated, IsJury))
def idea_rate(request, idea_id):
    """
    Endpoint to set, get and edit rates to an idea by a jury
    ---
    GET:
        response_serializer: ideas.serializers.IdeaScoreModelSerializer
    PATCH:
        serializer: ideas.serializers.IdeaScoreSerializer
        response_serializer: ideas.serializers.IdeaScoreModelSerializer
    POST:
        serializer: ideas.serializers.IdeaScoreSerializer
        response_serializer: ideas.serializers.IdeaScoreModelSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    user = request.user
    if request.method == "POST":
        serializer = IdeaScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = get_object_or_404(IdeaScoresCriteria, pk=serializer.validated_data['category_id'])
            value = serializer.validated_data['value']
            try:
                IdeaScores.objects.create(idea=idea, jury=user, category=category, value=value)
            except Exception as e:
                print(e)
                raise ValidationError({'detail': 'Ya fue evaluado en esta categoria.'})
    if request.method == "PATCH":
        serializer = IdeaScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = get_object_or_404(IdeaScoresCriteria, pk=serializer.validated_data['category_id'])
            value = serializer.validated_data['value']
            idea_score = get_object_or_404(IdeaScores, idea=idea, jury=user, category=category)
            idea_score.value = value
            idea_score.save()
    idea_scores = IdeaScores.objects.filter(idea=idea, jury=user)
    serializer = IdeaScoreModelSerializer(idea_scores, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
