from rest_framework import permissions


class IsJury(permissions.BasePermission):
    message = 'Jury restricted'

    def has_permission(self, request, view):
        return request.user and request.user.is_jury
