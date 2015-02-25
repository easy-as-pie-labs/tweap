from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project, Tag
import datetime


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

    # datetime.date.today() basically takes 00:00, so we want to show today for everything >= today() and < tomorrow()
    @classmethod
    def get_due_today_for_user(cls, user):
        return Event.objects.filter(attendees=user, start__gte=datetime.date.today(), start__lt=datetime.date.today() + datetime.timedelta(days=(1)))

    @classmethod
    def get_due_this_week_for_user(cls, user):
        end_of_week = datetime.date.today() + datetime.timedelta(days=(8)) # 8 because today() is today 00:00 and we need it to be 24:00
        return Event.objects.filter(attendees=user, start__lte=end_of_week, start__gte=datetime.date.today() + datetime.timedelta(days=(1)))

    def __str__(self):
        return self.title

    def get_start(self):

        if self.start is None:
            return ""
        year = self.start.year
        month = self.start.month
        day = self.start.day

        date = str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)

        hour = self.start.hour
        minute = self.start.minute

        time = str("%02d" % hour) + ":" + str("%02d" % minute)

        return date + " " + time

    def get_start_time_for_dashboard(self):
        hour = self.start.hour
        minute = self.start.minute

        time = str(hour) + ":" + str(minute)
        return time

    def get_start_datetime_for_dashboard(self):
        month = self.start.month
        day = self.start.day
        hour = self.start.hour
        minute = self.start.minute

        time = str(day) + "." + str(month) + ". " + str(hour) + ":" + str("%02d" % minute)
        return time


    def get_end(self):

        if self.end is None:
            return ""
        year = self.end.year
        month = self.end.month
        day = self.end.day

        date = str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)

        hour = self.end.hour
        minute = self.end.minute

        time = str("%02d" % hour) + ":" + str("%02d" % minute)

        return date + " " + time

    def get_start_for_cal(self):

        year = self.start.year
        month = self.start.month
        day = self.start.day

        date = str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)

        hour = self.start.hour
        minute = self.start.minute
        second = self.start.second

        time = str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % second)

        return date + "T" + time

    def get_end_for_cal(self):

        year = self.end.year
        month = self.end.month
        day = self.end.day

        date = str("%04d" % year) + "-" + str("%02d" % month) + "-" + str("%02d" % day)

        hour = self.end.hour
        minute = self.end.minute
        second = self.start.second

        time = str("%02d" % hour) + ":" + str("%02d" % minute) + ":" + str("%02d" % second)

        return date + "T" + time

    def remove_attendee(self, user):
        self.attendees.remove(user)
