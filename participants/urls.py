from django.conf.urls import url
from .views import user_detail, user_creation, user_update_password, CustomAuthToken


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
    url(r'^(?P<user_id>\d+)/update/password/$', user_update_password, name='user_update_password'),
    url(r'^authenticate/', CustomAuthToken.as_view()),
    url(r'^create/$', user_creation, name='user_creation'),
]
