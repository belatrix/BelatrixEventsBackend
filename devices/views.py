from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer


@api_view(['POST', ])
def android_device_registration(request):
    """
    Register device
    """
    device_code = (request.data['device_code'] if 'device_code' in request.data.keys() else None)
    devices = Device.objects.filter(device_code=device_code)
    if devices.count() == 0:
        device = Device.objects.create(device_code=device_code, type='android')
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        device = Device.objects.get(device_code=device_code)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
