from django.conf.urls import patterns, url
from project_management import views

urlpatterns = patterns(
    '',
    url(r'^new/$', views.Create.as_view(), name='create'),

)
