from django.db import models
from django.db import models
from django.contrib.auth.models import User
from os.path import splitext
from project_management.models import Project
import random
import hashlib


class Event(models.Model):
    text = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.text


class Url(models.Model):
    url = models.CharField(max_length=20, null=False)
    parameter = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.url + "/" + self.parameter

"""
TODO: url could also be multiple parameters
possible solution:

class Url(models.Model):
    url = models.CharField(max_length=20, null=False)

class UrlParameter(models.Model):
    value = models.CharField(max_length=20, null=False)
    url = models.ForeignKey(Url, null=False)

then in Notification:
def get_params():
    params = UrlParameter.objects.filter(url=url)
    parameters = []
    for param in params:
        parameters.append(param.value)
    return tuple(parameters)

then in ViewOne:
parameters = notification.get_params()
and:
arg = parameters
"""


class Notification(models.Model):
    receiver = models.ForeignKey(User, null=False, related_name='%(class)s_receiver')
    trigger = models.ForeignKey(User, null=False, related_name='%(class)s_triggerer')
    project = models.ForeignKey(Project, null=False)
    timestamp = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, null=False)
    url = models.ForeignKey(Url, null=False)

    def __str__(self):
        return self.trigger.username + "->" + self.receiver.username + " in " + self.project.name + ": " + self.event.text
