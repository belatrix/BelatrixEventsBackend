from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from uuid import uuid4

from .managers import UserManager


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=50)

    class Meta(object):
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    phone_regex = RegexValidator(
        regex=r'^\d{9}$',
        message="Phone number must be entered in the format: '999999999'. Up to 9 digits allowed.")
    # TODO: improve regexvalidator in order to support current contact mobile formats
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    role = models.ForeignKey(Role, blank=True, null=True)

    is_staff = models.BooleanField(_('is staff'), default=False)
    is_jury = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_blocked = models.BooleanField(default=False)

    is_password_reset_required = models.BooleanField(default=True)
    reset_password_code = models.UUIDField(default=None, blank=True, null=True)
    temporary_password = models.CharField(max_length=4, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def generate_reset_password_code(self):
        '''
        Returns UUID string to be sent by email when user require a password recovery action
        '''
        uuid_code = uuid4()
        self.reset_password_code = str(uuid_code)
        self.temporary_password = get_random_string(4, "hacktrx23456789")
        self.save()
        return self.reset_password_code


class Participant(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    event_id = models.IntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def creat_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
