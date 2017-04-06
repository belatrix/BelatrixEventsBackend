from .views import employee_detail
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<employee_id>\d+)/$', employee_detail, name='employee_detail'),
]
