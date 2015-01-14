from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns(
    '',
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^home/$', views.Home.as_view(), name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'user_management/login.html'},
        name='login',),
)
