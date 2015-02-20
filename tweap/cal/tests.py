from django.http import HttpResponseRedirect, request
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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

    def test_delete_event(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user_random = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name)
        project.save()
        project.members.add(user)
        project.save()

        event = Event(title=self.event_name, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})
        '''
        #Assign valid user
        assignees = [user_random.username]
        resp = self.client.post('/calendar/edit/' + str(event.id), {'title': "bla", 'description': "new Description", 'start_date': "", 'end_date': "", 'assignees': assignees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        # TODO: add test if notifications are deleted
        # target_url = request.build_absolute_uri(reverse('cal:edit', args=(event.id, )))
        '''

        event2 = Event(title=self.event_name2, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event2.save()

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # delete existing event
        resp = self.client.post('/calendar/delete/' + str(event.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        test_event = Event.objects.filter(id=event.id)
        self.assertFalse(test_event.exists())

        '''
            delete non existing event
        '''

        resp = self.client.post('/calendar/delete/9999')
        self.assertEqual(404, resp.status_code)

        # delete event while not in project
        # logout
        self.client.post('/users/logout')

        # login user_random
        self.client.post('/users/login/', {'username': 'testuser2', 'password': 'testpw'})

        # delete event
        resp = self.client.post('/calendar/delete/' + str(event2.id))
        self.assertEqual(404, resp.status_code)

        test_event2 = Event.objects.filter(id=event2.id)
        self.assertTrue(test_event2.exists())

        event.delete()
        event2.delete()
        project.delete()
        user.delete()
        user_random.delete()
        test_event.delete()
        test_event2.delete()