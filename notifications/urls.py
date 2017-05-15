from .views import send_message_by_city, get_all_messages, send_message_to_all
from django.conf.urls import url


urlpatterns = [
    url(r'^send/all/$', send_message_to_all, name='send_message_to_all'),
    url(r'^send/city/(?P<city_id>\d+)/$', send_message_by_city, name='send_message_by_city'),
    url(r'^all/$', get_all_messages, name='get_all_messages'),
]
