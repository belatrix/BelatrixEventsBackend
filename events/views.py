from random import randint
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event, Interaction
from .serializers import EventSerializer, InteractionSerializer


@api_view(['GET', ])
def event_detail(request, event_id):
    """
    Returns event list
    """
    event = get_object_or_404(Event, pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_featured(request):
    """
    Returns event featured
    """
    event_featured = Event.objects.filter(is_featured=True, is_active=True, is_upcoming=True).first()
    if event_featured == None:
        random_id = randint(0, Event.objects.count() - 1)
        event_featured = Event.objects.filter(is_active=True, is_upcoming=True)[random_id]
    serializer = EventSerializer(event_featured)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_interaction(request, event_id):
    """
    Returns event interactions
    """
    event = get_object_or_404(Event, pk=event_id)
    interactions = Interaction.objects.filter(event=event)
    serializer = InteractionSerializer(interactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_list(request):
    """
    Returns event list
    """
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_upcoming_list(request):
    """
    Returns upcoming event list
    """
    events = Event.objects.filter(is_upcoming=True)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_past_list(request):
    """
    Returns past event list
    """
    events = Event.objects.filter(is_upcoming=False)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
