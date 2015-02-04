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
    done = models.BooleanField(default=False)

    @classmethod
    def get_all_for_project(cls, project):
        return Todo.objects.filter(project=project)

    @classmethod
    def get_open_for_project(cls, project):
        return Todo.objects.filter(project=project, done=False)

    @classmethod
    def get_closed_for_project(cls, project):
        return Todo.objects.filter(project=project, done=True)

    @classmethod
    def get_all_for_user(cls, user):
        return Todo.objects.filter(assignees=user)

    @classmethod
    def get_open_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=False)

    @classmethod
    def get_closed_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=True)

    def __str__(self):
        return self.title

    def get_date(self):
        """
        get's compatible dateformat
        :return:
        """
        year = self.due_date.year
        month = self.due_date.month
        day = self.due_date.day
        return str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)