from django.contrib import admin
from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_code', 'type')


admin.site.register(Device, DeviceAdmin)
