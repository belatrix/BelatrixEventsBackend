from .views import device_registration
from django.conf.urls import url


urlpatterns = [
    url(r'^register/$', device_registration, name='registration'),
]
