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
    list_display = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'is_participant')}),
        ('Permissions', {'fields': ('groups',
                                    'user_permissions',
                                    'is_superuser',
                                    'is_staff',
                                    'is_active',)}),
        ('History', {'fields': ('date_joined', 'last_login')})
    )
    readonly_fields = ('date_joined',)
    ordering = ('email',)


admin.site.register(Participant)
admin.site.register(User, UserCustomAdmin)
