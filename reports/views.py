from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from events.models import Attendance, Event, Meeting, EventParticipant
from ideas.models import Idea, IdeaParticipant, IdeaVotes, IdeaScores


def index(request):
    return render(request, 'index.html')


def event_information(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    participants_registered = EventParticipant.objects.filter(event=event)
    attendances = Attendance.objects.filter(meeting__event=event).values('meeting__name').annotate(
        total=Count('participant')).order_by('total')
    ideas_proposed = Idea.objects.filter(event=event)
    ideas_valid = Idea.objects.filter(event=event, is_valid=True)
    team_members = IdeaParticipant.objects.filter(idea__event=event)
    votes = IdeaVotes.objects.filter(event=event)
    context = {'event': event,
               'participants_registered': participants_registered,
               'attendances': attendances,
               'ideas_proposed': ideas_proposed,
               'ideas_valid': ideas_valid,
               'team_members': team_members,
               'votes': votes}
    return render(request, 'event.html', context)


def participants_idea(request):
    participants_list = IdeaParticipant.objects.all()
    context = {'participants_list': participants_list}
    return render(request, 'participants_idea.html', context)


def idea_list(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    list = Idea.objects.filter(event=event, is_valid=True)
    context = {'idea_list': list}
    return render(request, 'idea_list.html', context)


def idea_in_development(request):
    list = Idea.objects.filter(is_completed=True)
    context = {'idea_list': list}
    return render(request, 'idea_list.html', context)


def idea_vote_results(request):
    results = IdeaVotes.objects.all().values('idea__title',
                                             'idea__id').annotate(total=Count('participant')).order_by('-total')
    context = {'results': results}
    return render(request, 'idea_vote_results.html', context)


def idea_jury_results(request):
    results = IdeaScores.objects.all().order_by('idea')
    context = {'results': results}
    return render(request, 'idea_jury_results.html', context)


def meeting_list(request):
    meetings = Meeting.objects.all()
    context = {'meeting_list': meetings}
    return render(request, 'meeting_list.html', context)


def meeting_attendance_detail(request, meeting_id):
    attendance_list = Attendance.objects.filter(meeting=meeting_id)
    context = {'attendance_list': attendance_list}
    return render(request, 'attendance_list.html', context)
