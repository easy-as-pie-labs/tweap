from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns(
    '',
    url(r'^$', views.Home.as_view(), name='home'),
)
