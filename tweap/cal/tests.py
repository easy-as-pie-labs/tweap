from django.http import HttpResponseRedirect
from django.test import TestCase
from django.contrib.auth.models import User
from project_management.models import Project
from cal.models import Event
from datetime import datetime
import pytz


class ModelTest(TestCase):

    project_name = "Testproject"
    project_name2 = "Testproject2"
    event_name = "Testevent"
    event_name2 = "Testevent2"

    def test_get_all_for_project(self):
        project = Project(name=self.project_name)
        project.save()
        project2 = Project(name=self.project_name2)
        project2.save()

        # no event so there must be an empty result
        self.assertEquals(Event.get_all_for_project(project).count(), 0)
        self.assertEquals(Event.get_all_for_project(project2).count(), 0)

        event = Event(title=self.event_name, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event.save()

        # test stringify method of Event
        self.assertEqual(str(event), self.event_name)

        # test if event is found by project
        self.assertEquals(Event.get_all_for_project(project).count(), 1)
        self.assertEquals(Event.get_all_for_project(project2).count(), 0)

        # cleanup
        event.delete()
        project.delete()
        project2.delete()

    def test_get_all_for_user(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name)
        project.save()
        event = Event(title=self.event_name, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event.save()

        # user is not assigned so the result must be empty
        self.assertEquals(Event.get_all_for_user(user).count(), 0)
        self.assertEquals(Event.get_all_for_user(user2).count(), 0)

        event.attendees.add(user)
        event.save()

        # now event must be found by user
        self.assertEquals(Event.get_all_for_user(user).count(), 1)
        self.assertEquals(Event.get_all_for_user(user2).count(), 0)

        # cleanup
        event.delete()
        project.delete()
        user.delete()
        user2.delete()