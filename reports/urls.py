from django.conf.urls import url

from .views import index
from .views import idea_list, idea_in_development
from .views import meeting_attendance_detail, meeting_list
from .views import participants_idea


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^participants/idea/$', participants_idea, name='participants_idea'),
    url(r'^event/(?P<event_id>\d+)/idea/list/$', idea_list, name='idea_list'),
    url(r'^idea/development/list/$', idea_in_development, name='ideas_in_development'),
    url(r'^meeting/list/$', meeting_list, name='meeting_list'),
    url(r'^meeting/(?P<meeting_id>\d+)/attendance/list/$', meeting_attendance_detail, name='attendance_list'),
]
