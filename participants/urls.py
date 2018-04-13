from django.conf.urls import url
from .views import user_detail


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', user_detail, name='user_detail'),
]
