from django.conf.urls import url
from .views import user_detail, user_creation, user_update_password, CustomAuthToken
from .views import user_password_recovery_request, user_password_recovery_confirmation


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
    url(r'^(?P<user_id>\d+)/update/password/$', user_update_password, name='user_update_password'),
    url(r'^authenticate/', CustomAuthToken.as_view()),
    url(r'^create/$', user_creation, name='user_creation'),
    url(r'^recover/$', user_password_recovery_request, name='user_password_recovery_request'),
    url(r'^recover/(?P<user_uuid>[0-9a-z-]+)$',
        user_password_recovery_confirmation,
        name='user_password_recovery_confirmation'),
]
