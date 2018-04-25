from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from events.models import Event
from participants.models import User

from .models import Idea, IdeaParticipant
from .serializers import IdeaCreationSerializer, IdeaSerializer, IdeaParticipantsSerializer
from .serializers import IdeaRegistrationSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def idea(request, idea_id):
    """
    Endpoint for ideas
    ---
    GET:
        serializer: ideas.serializers.IdeaSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    serializer = IdeaSerializer(idea)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
            title = serializer.data['title']
            description = serializer.data['description']
            try:
                new_idea = Idea.objects.create(author=author, event=event, title=title, description=description)
            except Exception as e:
                print(e)
                raise NotAcceptable('Esta idea ya existe.')
            serializer = IdeaSerializer(new_idea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def idea_participants(request, idea_id):
    """
    Endpoint to get participant list group by idea
    ---
    GET:
        serializer: ideas.serializers.IdeaParticipantsSerializer
    """
    idea = get_object_or_404(Idea, pk=idea_id)
    participants = get_list_or_404(IdeaParticipant, idea=idea)
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
        try:
            IdeaParticipant.objects.create(idea=idea, user=user)
        except Exception as e:
            print(e)
            raise NotAcceptable('Ya registrado.')
        participants = get_list_or_404(IdeaParticipant, idea=idea)
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
        participants = get_list_or_404(IdeaParticipant, idea=idea)
        serializer = IdeaParticipantsSerializer(participants, many=True)
        return Response({"is_registered": False,
                         "team_members": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def idea_list(request, event_id):
    """
    Returns idea list by event
    ---
    GET:
        response_serializer: ideas.serializers.IdeaSerializer
    """
    ideas = get_list_or_404(Idea, event=event_id)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
