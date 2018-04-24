from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Idea
from .serializers import IdeaSerializer


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


@api_view(['GET'])
def idea_list(request, event_id):
    """
    Returns idea list by event
    ---
    GET:
        serializer: ideas.serializers.IdeaSerializer
    """
    ideas = get_list_or_404(Idea, event=event_id)
    serializer = IdeaSerializer(ideas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
