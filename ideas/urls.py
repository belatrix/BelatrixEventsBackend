from django.conf.urls import url
from .views import idea, idea_create, idea_register, idea_participants, idea_unregister
from .views import idea_vote, idea_completed, idea_open


urlpatterns = [
    url(r'^(?P<idea_id>\d+)/$', idea, name='idea'),
    url(r'^(?P<idea_id>\d+)/completed/$', idea_completed, name='idea_completed'),
    url(r'^(?P<idea_id>\d+)/open/$', idea_open, name='idea_open'),
    url(r'^(?P<idea_id>\d+)/register/$', idea_register, name='idea_register'),
    url(r'^(?P<idea_id>\d+)/unregister/$', idea_unregister, name='idea_unregister'),
    url(r'^(?P<idea_id>\d+)/participants/$', idea_participants, name='idea_participants'),
    url(r'^(?P<idea_id>\d+)/vote/$', idea_vote, name='idea_vote'),
    url(r'^create/$', idea_create, name='idea_create'),
    # url(r'^list/event/(?P<event_id>\d+)/$', idea_list, name='idea_list'),
]
