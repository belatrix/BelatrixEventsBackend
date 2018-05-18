from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from events.models import Attendance, Event, Meeting
from ideas.models import Idea, IdeaParticipant, IdeaVotes


def index(request):
    return render(request, 'index.html')


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


def meeting_list(request):
    meetings = Meeting.objects.all()
    context = {'meeting_list': meetings}
    return render(request, 'meeting_list.html', context)


def meeting_attendance_detail(request, meeting_id):
    attendance_list = Attendance.objects.filter(meeting=meeting_id)
    context = {'attendance_list': attendance_list}
    return render(request, 'attendance_list.html', context)
