from .views import android_device_registration
from django.conf.urls import url


urlpatterns = [
    url(r'^register/android/$', android_device_registration, name='android_registration'),
]
