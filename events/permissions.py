from rest_framework import permissions

from .models import Attendance


class IsAttendee(permissions.BasePermission):
    message = 'Attendee restricted'

    def has_permission(self, request, view):
        attendees = Attendance.objects.filter(participant__email=request.user.email).count()
        if attendees > 0:
            return True
