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
    assignees = models.ManyToManyField(User)
    project = models.ForeignKey(Project)
    tags = models.ManyToManyField(Tag)
