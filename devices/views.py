from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer


@api_view(['POST', ])
def device_registration(request, device_code):
    """
    Register device
    """
    devices = Device.objects.filter(device_code=device_code)
    if devices.count() == 0:
        device = Device.objects.create(device_code=device_code)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        device = Device.objects.get(device_code=device_code)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
