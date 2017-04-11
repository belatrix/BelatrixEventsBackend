from .views import device_registration
from django.conf.urls import url


urlpatterns = [
    url(r'^register/(?P<device_code>\w+)/$', device_registration, name='registration'),
]
