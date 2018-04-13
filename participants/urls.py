from django.conf.urls import url
from .views import user_detail, user_creation


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
    url(r'^create/$', user_creation, name='user_creation'),
]
