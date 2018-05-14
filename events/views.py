from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.random_item import random_element_list

from participants.permissions import IsStaff

from .models import Event, Interaction, City, Meeting
from .serializers import CitySerializer, EventSerializer, InteractionSerializer, MeetingSerializer


@api_view(['GET', ])
def event_city_list(request):
    """
    Returns event city list
    """
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    ---
    GET:
        parameters:
            - name: city
              description: set city_id to filter events by city
              type: string
              required: false
              paramType: query
    """
    events = Event.objects.filter(is_active=True, is_featured=True)

    if request.GET.get('city'):
        city_id = int(request.GET.get('city'))
        city = get_object_or_404(City, pk=city_id)
        events_city = events.filter(city__in=[city])
        if events_city.count() > 0:
            events = events_city
        else:
            events = Event.objects.filter(is_active=True, city__in=[city])

    if events.count() > 0:
        events_upcoming = events.filter(is_upcoming=True)
        if events_upcoming.count() > 0:
            if events_upcoming.count() > 1:
                event_featured = random_element_list(events_upcoming)
            else:
                event_featured = events_upcoming[0]
        else:
            event_featured = random_element_list(events)
    else:
        events = Event.objects.filter(is_active=True)
        if events.count() > 0:
            event_featured = random_element_list(events)
        else:
            Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event_featured)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def event_interaction(request, event_id):
    """
    Returns event interactions
    ---
    GET:
        parameters:
            - name: pagination
              description: set true if you want paginated results
              type: string
              required: false
              paramType: query
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
    ---
    GET:
        parameters:
            - name: city
              description: set city_id to filter events by city
              type: string
              required: false
              paramType: query
    """
    events = Event.objects.all()
    if request.GET.get('city'):
        city_id = int(request.GET.get('city'))
        city = get_object_or_404(City, pk=city_id)
        events = Event.objects.filter(city__in=[city])
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
    ---
    GET:
        parameters:
            - name: city
              description: set city_id to filter events by city
              type: string
              required: false
              paramType: query
    """
    events = Event.objects.filter(is_upcoming=True, is_active=True)
    if request.GET.get('city'):
        city_id = int(request.GET.get('city'))
        city = get_object_or_404(City, pk=city_id)
        events = events.filter(city__in=[city])
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
    ---
    GET:
        parameters:
            - name: city
              description: set city_id to filter events by city
              type: string
              required: false
              paramType: query
    """
    events = Event.objects.filter(is_upcoming=False, is_active=True)
    if request.GET.get('city'):
        city_id = int(request.GET.get('city'))
        city = get_object_or_404(City, pk=city_id)
        events = events.filter(city__in=[city])
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
@permission_classes((IsAuthenticated, IsStaff))
def meeting_list(request):
    """
    Returns meetings list to register attendance
    ---
    GET:
        response_serializer: events.serializers.MeetingSerializer
    """
    meetings = Meeting.objects.all().filter(is_active=True)
    serializer = MeetingSerializer(meetings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
