from .views import android_device_registration, update_device_city
from django.conf.urls import url


urlpatterns = [
    url(r'^register/android/$', android_device_registration, name='android_registration'),
    url(r'^update/city/$', update_device_city, name='update_device_city'),
]
