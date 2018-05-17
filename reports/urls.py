from django.conf.urls import url

from .views import index
from .views import idea_list
from .views import participants_idea

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^participants/idea/$', participants_idea, name='participants_idea'),
    url(r'^event/(?P<event_id>\d+)/idea/list/$', idea_list, name='idea_list'),
]
