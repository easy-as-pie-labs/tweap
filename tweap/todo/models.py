from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from project_management.models import Project, Tag


class Todo(models.Model):
    """
    Model for Todos
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    assignees = models.ManyToManyField(User, null=True, blank=True)
    project = models.ForeignKey(Project)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    @classmethod
    def get_for_project(cls, project):
        return Todo.objects.filter(project=project)

    @classmethod
    def get_for_user(cls, user):
        return Todo.objects.filter(assignees=user)

    def __str__(self):
        return self.title