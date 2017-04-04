from django.contrib import admin
from .models import Event, Interaction, Location


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'image', 'details', 'is_upcoming')


class InteractionAdmin(admin.ModelAdmin):
    list_display = ('text', 'event', 'votes')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


admin.site.register(Event, EventAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Location, LocationAdmin)
