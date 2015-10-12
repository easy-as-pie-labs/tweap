from django.conf.urls import patterns, url
from chat import views

urlpatterns = patterns(
    '',
    url(r'^api/$', views.api, name='api'),
)
