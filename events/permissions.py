from rest_framework import permissions
from rest_framework.compat import is_authenticated

from .models import Attendance


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAttendee(permissions.BasePermission):
    message = 'Attendee restricted'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return (
                    request.method in SAFE_METHODS or
                    request.user and
                    is_authenticated(request.user)
            )
        attendees = Attendance.objects.filter(participant__email=request.user.email).count()
        if attendees > 0:
            return True
