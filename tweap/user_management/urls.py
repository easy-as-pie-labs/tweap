from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns(
    '',
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),

)
