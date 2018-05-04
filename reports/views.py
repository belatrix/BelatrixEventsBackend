from django.shortcuts import render

from ideas.models import IdeaParticipant


def index(request):
    return render(request, 'index.html')


def participants_idea(request):
    participants_list = IdeaParticipant.objects.all()
    context = {'participants_list': participants_list}
    return render(request, 'participants_idea.html', context)
