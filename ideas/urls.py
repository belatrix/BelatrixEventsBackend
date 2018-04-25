from django.conf.urls import url
from .views import idea, idea_create, idea_register, idea_participants, idea_unregister


urlpatterns = [
    url(r'^(?P<idea_id>\d+)/$', idea, name='idea'),
    url(r'^(?P<idea_id>\d+)/register/$', idea_register, name='idea_register'),
    url(r'^(?P<idea_id>\d+)/unregister/$', idea_unregister, name='idea_unregister'),
    url(r'^(?P<idea_id>\d+)/participants/$', idea_participants, name='idea_participants'),
    url(r'^create/$', idea_create, name='idea_create'),
    # url(r'^list/event/(?P<event_id>\d+)/$', idea_list, name='idea_list'),
]
