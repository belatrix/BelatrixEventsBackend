from django.contrib import admin
from .models import City, Event, Interaction, Location, EventParticipant


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime', 'image', 'details', 'is_upcoming', 'is_featured', 'get_cities')


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'participant')


class InteractionAdmin(admin.ModelAdmin):
    list_display = ('text', 'event', 'votes')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


admin.site.register(City, CityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Location, LocationAdmin)
