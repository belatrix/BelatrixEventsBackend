from rest_framework import permissions

from .models import Participant


class IsJury(permissions.BasePermission):
    message = 'Jury restricted'

    def has_permission(self, request, view):
        return request.user and request.user.is_jury


class IsParticipant(permissions.BasePermission):
    message = 'User needs to be a participant registered.'

    def has_permission(self, request, view):
        participants = Participant.objects.filter(email=request.user.email).count()
        if participants > 0:
            return True


class IsModerator(permissions.BasePermission):
    message = 'User needs to be a moderator.'

    def has_permission(self, request, view):
        return request.user and request.user.is_moderator
