from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea, IdeaParticipant, IdeaVotes, IdeaScoresCriteria, IdeaScores


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_completed')


class IdeaParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')


class IdeaVotesAdmin(admin.ModelAdmin):
    list_display = ('participant', 'idea', 'event')


class IdeaScoresCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')


class IdeaScoresAdmin(admin.ModelAdmin):
    list_display = ('idea', 'jury', 'category', 'value')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaParticipant, IdeaParticipantAdmin)
admin.site.register(IdeaVotes, IdeaVotesAdmin)
admin.site.register(IdeaScoresCriteria, IdeaScoresCriteriaAdmin)
admin.site.register(IdeaScores, IdeaScoresAdmin)
