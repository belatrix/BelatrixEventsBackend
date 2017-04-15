from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    GOOGLE_QR_CHART_URL = 'https://chart.apis.google.com/chart?cht=qr&chs=500x500&chl='

    employee_qr_code = serializers.SerializerMethodField('qr_code')

    def qr_code(self, employee):
        return self.GOOGLE_QR_CHART_URL + str(employee.pk)

    class Meta(object):
        model = Employee
        fields = ('id', 'name', 'avatar', 'email', 'role', 'twitter', 'github', 'website', 'employee_qr_code')
