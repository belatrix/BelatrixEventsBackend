from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from devices.models import Device
from .models import Message
from .serializers import MessageSerializer
from utils import send_messages


@api_view(['POST', ])
def send_message_to_all(request):
    """
    Creates a message to all devices by city
    """
    devices = Device.objects.all()
    message_text = (request.data['message'] if 'message' in request.data.keys() else None)
    if message_text is not None:
        message = Message.objects.create(text=message_text, city=0)
        if devices.count() > 0:
            send_messages.send_push_notification(devices, message.text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def send_message_by_city(request, city_id):
    """
    Creates a message to all devices by city
    """
    devices = Device.objects.filter(city=city_id) | Device.objects.filter(city=0)
    message_text = (request.data['message'] if 'message' in request.data.keys() else None)
    if message_text is not None:
        message = Message.objects.create(text=message_text, city=city_id)
        if devices.count() > 0:
            send_messages.send_push_notification(devices, message.text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def get_all_messages(request):
    """
     Return a message list per city
    """
    messages = Message.objects.filter(is_active=True)
    if request.GET.get('city'):
        city_id = int(request.GET.get('city'))
        messages = messages.filter(city=city_id)

    if request.GET.get('pagination'):
        pagination = request.GET.get('pagination')
        if pagination == 'true':
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(messages, request)
            serializer = MessageSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
    else:
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
