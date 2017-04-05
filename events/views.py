from random import randint
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
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
    if event_featured is None:
        random_id = randint(0, Event.objects.count() - 1)
        event_featured = Event.objects.filter(is_active=True, is_upcoming=True)[random_id]
    serializer = EventSerializer(event_featured)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_interaction(request, event_id):
    """
    Returns event interactions
    """
    event = get_object_or_404(Event, pk=event_id, is_active=True)
    interactions = Interaction.objects.filter(event=event, is_active=True)
    if request.GET.get('pagination'):
        pagination = request.GET.get('pagination')
        if pagination == 'true':
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(interactions, request)
            serializer = InteractionSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', ])
def event_interaction_vote(request, interaction_id):
    """
    Add +1 vote to interaction votes count
    """
    interaction = get_object_or_404(Interaction, pk=interaction_id, is_active=True)
    if interaction.event.is_interaction_active:
        interaction.votes += 1
        interaction.save()
    serializer = InteractionSerializer(interaction)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['GET', ])
def event_list(request):
    """
    Returns event list
    """
    events = Event.objects.all()
    if request.GET.get('pagination'):
        pagination = request.GET.get('pagination')
        if pagination == 'true':
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(events, request)
            serializer = EventSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_upcoming_list(request):
    """
    Returns upcoming event list
    """
    events = Event.objects.filter(is_upcoming=True, is_active=True)
    if request.GET.get('pagination'):
        pagination = request.GET.get('pagination')
        if pagination == 'true':
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(events, request)
            serializer = EventSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_past_list(request):
    """
    Returns past event list
    """
    events = Event.objects.filter(is_upcoming=False, is_active=True)
    if request.GET.get('pagination'):
        pagination = request.GET.get('pagination')
        if pagination == 'true':
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(events, request)
            serializer = EventSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
