from rest_framework import permissions
from rest_framework.compat import is_authenticated

from .models import Participant


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsJury(permissions.BasePermission):
    message = 'Jury restricted'

    def has_permission(self, request, view):
        return request.user and request.user.is_jury


class IsParticipant(permissions.BasePermission):
    message = 'User needs to be a participant registered.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return (
                    request.method in SAFE_METHODS or
                    request.user and
                    is_authenticated(request.user)
            )
        participants = Participant.objects.filter(email=request.user.email).count()
        if participants > 0:
            return True


class IsModerator(permissions.BasePermission):
    message = 'User needs to be a moderator.'

    def has_permission(self, request, view):
        return request.user and request.user.is_moderator


class IsStaff(permissions.BasePermission):
    message = 'Staff restricted'

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
