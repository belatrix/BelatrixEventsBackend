from django.conf.urls import url

from .views import index
from .views import participants_idea

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^participants/idea/$', participants_idea, name='participants_idea'),
]
