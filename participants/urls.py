from django.conf.urls import url
from .views import user_detail, user_creation, CustomAuthToken


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
    url(r'^authenticate/', CustomAuthToken.as_view()),
    url(r'^create/$', user_creation, name='user_creation'),
]
