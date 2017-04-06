from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer


@api_view(['GET', ])
def employee_detail(request, employee_id):
    """
    Returns employee detail
    """
    employee = get_object_or_404(Employee, pk=employee_id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)
