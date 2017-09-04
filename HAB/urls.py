from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^actuate/device(?P<device>[0-9]+)/state(?P<state>[0-9]+)/$', views.actuation, name='async'),
]
