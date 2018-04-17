from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404
from participants.models import User, Participant


class Command(BaseCommand):
    help = "Check if a User is a participant registered, if so set True is_participant for User"

    def check_participant(self):
        participants = get_list_or_404(Participant)
        for participant in participants:
            user = User.objects.filter(email=participant.email)
            if len(user) == 1:
                user_registered = user[0]
                user_registered.is_participant = True
                user_registered.save()

    def handle(self, *args, **options):
        self.check_participant()
