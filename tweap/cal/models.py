from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project, Tag


class Event(models.Model):
    """
    Model for Events
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=200)
    attendees = models.ManyToManyField(User, null=True, blank=True)
    project = models.ForeignKey(Project)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    class Meta:
        ordering = ['start', 'project__name']

    @classmethod
    def get_all_for_project(cls, project):
        return Event.objects.filter(project=project)

    @classmethod
    def get_all_for_user(cls, user):
        return Event.objects.filter(attendees=user)

    def __str__(self):
        return self.title