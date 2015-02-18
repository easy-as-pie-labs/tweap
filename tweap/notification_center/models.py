from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project


class NotificationEvent(models.Model):
    text = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.text


class Notification(models.Model):
    receiver = models.ForeignKey(User, null=False, related_name='%(class)s_receiver')
    trigger_user = models.ForeignKey(User, null=False, related_name='%(class)s_triggerer')
    timestamp = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, null=False)
    target_url = models.CharField(max_length=100, blank=False)
    event = models.ForeignKey(NotificationEvent, null=False)

    def __str__(self):
        return str(self.event) + ", from " + self.trigger_user.username + ", to " + self.receiver.username
