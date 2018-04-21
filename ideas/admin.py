from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea, IdeaParticipant


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'event')


class IdeaParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaParticipant, IdeaParticipantAdmin)
