from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer


@api_view(['GET', ])
def event_detail(request, event_id):
    """
    Returns event list
    """
    event = get_object_or_404(Event, pk=event_id)
    serializer = EventSerializer(event)
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
