from django.contrib import admin
from .models import Event, Interaction


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'image', 'details', 'is_upcoming')


class InteractionAdmin(admin.ModelAdmin):
    list_display = ('text', 'event', 'votes')


admin.site.register(Event, EventAdmin)
admin.site.register(Interaction, InteractionAdmin)
