from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Idea


class IdeaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'event')


admin.site.register(Idea, IdeaAdmin)
