from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404, get_object_or_404
from events.models import EventParticipant, Event
from participants.models import User, Participant


class Command(BaseCommand):
    help = "Check if a User is a participant registered, if so set True is_participant for User"

    def add_arguments(self, parser):
        parser.add_argument('--event', dest='event_id', required=True, help='Event ID')

    def check_participant(self, event_id):
        event = get_object_or_404(Event, pk=event_id)
        participants = get_list_or_404(Participant, event_id=event_id)
        for participant in participants:
            user = User.objects.filter(email=participant.email)
            if len(user) == 1:
                user_registered = user[0]
                user_registered.full_name = participant.full_name
                user_registered.save()
                EventParticipant.objects.create(event=event, participant=user_registered)

    def handle(self, *args, **options):
        event_id = options['event_id']
        self.check_participant(event_id)
