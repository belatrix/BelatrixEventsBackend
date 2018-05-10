from django.conf.urls import url
from .views import user_profile, user_detail
from .views import user_creation, user_update, user_update_password, CustomAuthToken
from .views import user_password_recovery_request, user_password_recovery_confirmation, user_logout
from ideas.views import my_ideas


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
    url(r'^authenticate/', CustomAuthToken.as_view()),
    url(r'^create/$', user_creation, name='user_creation'),
    url(r'^logout/$', user_logout, name='user_logout'),
    url(r'^profile/$', user_profile, name='user_profile'),
    url(r'^ideas/$', my_ideas, name='my_ideas'),
    url(r'^recover/$', user_password_recovery_request, name='user_password_recovery_request'),
    url(r'^update/$', user_update, name='user_update'),
    url(r'^update/password/$', user_update_password, name='user_update_password'),
    url(r'^recover/(?P<user_uuid>[0-9a-z-]+)$',
        user_password_recovery_confirmation,
        name='user_password_recovery_confirmation'),
]
