from django.contrib.auth.models import User
from django.db import models
import datetime
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
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', 'project__name']

    @classmethod
    def get_all_for_project(cls, project):
        return Todo.objects.filter(project=project)

    @classmethod
    def get_open_for_project(cls, project):
        return Todo.objects.filter(project=project, done=False)

    @classmethod
    def get_open_overdue_for_project(cls, project):
        return Todo.objects.filter(project=project, done=False, due_date__isnull=False, due_date__lt=datetime.date.today())

    @classmethod
    def get_open_due_today_for_project(cls, project):
        return Todo.objects.filter(project=project, done=False, due_date__isnull=False, due_date=datetime.date.today())

    @classmethod
    def get_closed_for_project(cls, project):
        return Todo.objects.filter(project=project, done=True).order_by('-completed_date', 'title')

    @classmethod
    def get_open_rest_for_project(cls, project):
        return Todo.objects.filter(project=project, done=False, due_date__isnull=False, due_date__gt=datetime.date.today()) | Todo.objects.filter(project=project, done=False, due_date__isnull=True)

    @classmethod
    def get_all_for_user(cls, user):
        return Todo.objects.filter(assignees=user)

    @classmethod
    def get_open_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=False)

    @classmethod
    def get_closed_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=True)

    @classmethod
    def get_overdue_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=False, due_date__isnull=False, due_date__lt=datetime.date.today())

    @classmethod
    def get_due_today_for_user(cls, user):
        return Todo.objects.filter(assignees=user, done=False, due_date__isnull=False, due_date=datetime.date.today())

    @classmethod
    def get_due_this_week_for_user(cls, user):
        end_of_week = datetime.date.today() + datetime.timedelta(days=(7))
        return Todo.objects.filter(assignees=user, done=False, due_date__isnull=False, due_date__lte=end_of_week, due_date__gt=datetime.date.today())

    def __str__(self):
        return self.title

    def get_date(self):
        """
        get's compatible dateformat
        :return:
        """
        if self.due_date is None:
            return ""
        year = self.due_date.year
        month = self.due_date.month
        day = self.due_date.day
        return str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)

    def get_date_for_dashboard(self):
        month = self.due_date.month
        day = self.due_date.day
        time = str(day) + "." + str(month) + "."
        return time

    def remove_assignee(self, user):
        self.assignees.remove(user)
