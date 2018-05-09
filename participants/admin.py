from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export.admin import ImportExportMixin
from .models import Participant, User


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password using "
                                                    "<a href=\'../password/\'>this form</a>."))

    class Meta(object):
        model = User
        fields = ('email',)

    def clean_password(self):
        return self.initial['password']


class UserCustomAdmin(ImportExportMixin, BaseUserAdmin):
    form = UserChangeForm
    list_display = ("email", "full_name", "is_staff", "is_moderator", "is_jury", "is_password_reset_required")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'full_name',)}),
        ('Permissions', {'fields': ('is_superuser',
                                    'is_staff',
                                    'is_moderator',
                                    'is_active',
                                    'is_blocked',
                                    'is_jury',
                                    'groups',
                                    'user_permissions')}),
        ('Security options', {'fields': ('is_password_reset_required',
                                         'reset_password_code',
                                         'temporary_password')}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined',)
    ordering = ('email',)


class ParticipantForm(ImportExportMixin, admin.ModelAdmin):
    list_display = ("email", "full_name", "event_id")


admin.site.register(Participant, ParticipantForm)
admin.site.register(User, UserCustomAdmin)
