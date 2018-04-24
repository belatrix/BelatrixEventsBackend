from .views import event_detail, event_list, event_upcoming_list, event_past_list, event_featured, event_city_list
# from .views import event_interaction, event_interaction_vote
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<event_id>\d+)/$', event_detail, name='event_detail'),
    # url(r'^(?P<event_id>\d+)/interaction/list/$', event_interaction, name='event_interaction'),
    url(r'^city/list/$', event_city_list, name='event_city_list'),
    url(r'^featured/$', event_featured, name='event_featured'),
    # url(r'^interaction/(?P<interaction_id>\d+)/vote$', event_interaction_vote, name='event_interaction_vote'),
    url(r'^list/$', event_list, name='event_list'),
    url(r'^upcoming/list/$', event_upcoming_list, name='event_upcoming_list'),
    url(r'^past/list/$', event_past_list, name='event_past_list'),
]
