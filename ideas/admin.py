from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea, IdeaParticipant, IdeaVotes


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_completed')


class IdeaParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')


class IdeaVotesAdmin(admin.ModelAdmin):
    list_display = ('participant', 'idea', 'event')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaParticipant, IdeaParticipantAdmin)
admin.site.register(IdeaVotes, IdeaVotesAdmin)
