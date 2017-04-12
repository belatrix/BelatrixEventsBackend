from django.contrib import admin
from .models import Message
from utils.send_messages import send_push_notification
from devices.models import Device


class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'city')

    def save_model(self, request, obj, form, change):
        devices = Device.objects.filter(city=obj.city)
        send_push_notification(devices, obj.text)
        obj.save()


admin.site.register(Message, MessageAdmin)
