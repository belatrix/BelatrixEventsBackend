from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea, IdeaVotes, IdeaScoresCriteria, IdeaScores
from .models import IdeaParticipant, IdeaCandidate


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_valid', 'is_completed')


class IdeaParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea')


class IdeaCandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'is_accepted')


class IdeaVotesAdmin(admin.ModelAdmin):
    list_display = ('participant', 'idea', 'event')


class IdeaScoresCriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')


class IdeaScoresAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('idea', 'jury', 'category', 'value')


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaParticipant, IdeaParticipantAdmin)
admin.site.register(IdeaCandidate, IdeaCandidateAdmin)
admin.site.register(IdeaVotes, IdeaVotesAdmin)
admin.site.register(IdeaScoresCriteria, IdeaScoresCriteriaAdmin)
admin.site.register(IdeaScores, IdeaScoresAdmin)
