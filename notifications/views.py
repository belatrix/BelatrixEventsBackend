from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.models import City
from devices.models import Device
from .models import Message
from .serializers import MessageSerializer
from utils import send_messages


@api_view(['POST', ])
def send_message_by_city(request, city_id):
    """
    Creates a message to all devices by city
    """
    city = get_object_or_404(City, pk=city_id)
    devices = Device.objects.filter(city=city.id)
    message_text = (request.data['message'] if 'message' in request.data.keys() else None)
    if message_text is not None:
        message = Message.objects.create(text=message_text)
        if devices.count() > 0:
            send_messages.send_push_notification(devices, message.text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
