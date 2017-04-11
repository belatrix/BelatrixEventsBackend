from .views import send_message_by_city
from django.conf.urls import url


urlpatterns = [
    url(r'^send/city/(?P<city_id>\d+)/$', send_message_by_city, name='send_message_by_city'),
]
