from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project, Tag
import datetime
import pytz


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
    def get_start_today_for_user(cls, user):
        now = datetime.datetime.now(pytz.utc)
        now = now - datetime.timedelta(days=(1))

        # fixes strange bug where 00:00 was included even though it's supposed to be less than (not equals)
        now = now.replace(hour=23, minute=59, second=59)
        tomorrow = now + datetime.timedelta(days=(1))
        #tomorrow = tomorrow.replace(hour=0,minute=0,second=0)
        return Event.objects.filter(attendees=user, start__gte=now, start__lt=tomorrow)


    @classmethod
    def get_start_this_week_for_user(cls, user):
        now = datetime.datetime.now(pytz.utc)
        today = now.replace(hour=0,minute=0,second=0)
        # fixes strange bug where 00:00 wasn't included even though it's supposed to be less than and equals
        tomorrow = now.replace(hour=23, minute=59, second=59)
        end_of_week = today + datetime.timedelta(days=(7))
        return Event.objects.filter(attendees=user, start__lt=end_of_week, start__gte=tomorrow)

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

        time = str(hour) + ":" + str("%02d" % minute)
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
