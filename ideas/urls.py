from django.conf.urls import url
from .views import idea, idea_create, idea_list


urlpatterns = [
    url(r'^(?P<idea_id>\d+)/$', idea, name='idea'),
    url(r'^create/$', idea_create, name='idea_create'),
    url(r'^list/event/(?P<event_id>\d+)/$', idea_list, name='idea_list'),
]
