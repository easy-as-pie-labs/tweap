from django.http import HttpResponseRedirect, request, HttpResponse
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

class ViewTests(TestCase):
    project_name = "Testproject"
    project_name2 = "Testproject2"
    project_description = "Testdescription"
    event_name = "Testevent"
    test_start_date = "2015-02-25 13:37"
    test_end_date = "2015-02-25 14:37"

    def test_create_event(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')

        project_assigned = Project(name=self.project_name, description=self.project_description)
        project_assigned.save()
        project_assigned.members.add(user)
        project_assigned.save()

        project_unassigned = Project(name=self.project_name, description=self.project_description)
        project_unassigned.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #User is assigned to project (GET)
        resp = self.client.get('/calendar/new/project/' + str(project_assigned.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        #User is assigned to project and Title, start_date and end_date is not empty
        resp = self.client.post('/calendar/new/project/' + str(project_assigned.id), {'title': self.event_name, 'description': self.project_description, 'start': self.test_start_date, 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        event = Event.objects.filter(title=self.event_name)
        self.assertTrue(event.exists())
        event.delete()

        #User is assigned to project but Title is empty
        resp = self.client.post('/calendar/new/project/' + str(project_assigned.id), {'title': "", 'description': self.project_description, 'start': self.test_start_date, 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #User is assigned to project but start_date is empty
        resp = self.client.post('/calendar/new/project/' + str(project_assigned.id), {'title': self.event_name, 'description': self.project_description, 'start': "", 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #User is assigned to project but end_date is empty
        resp = self.client.post('/calendar/new/project/' + str(project_assigned.id), {'title': self.event_name, 'description': self.project_description, 'start': self.test_start_date, 'end': "", 'location': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #User is assigned to project but start_date is bigger than end_date
        resp = self.client.post('/calendar/new/project/' + str(project_assigned.id), {'title': self.event_name, 'description': self.project_description, 'start': self.test_end_date, 'end': self.test_start_date, 'location': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #User is unassigned to project(GET)
        resp = self.client.get('/calendar/new/project' + str(project_unassigned.id))
        self.assertEqual(404, resp.status_code)

        #User is unassigned to project and Title is not empty
        resp = self.client.post('/calendar/new/project/' + str(project_unassigned.id), {'title': self.event_name, 'description': self.project_description, 'start': self.test_start_date, 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #User is unassigned to project and Title is empty
        resp = self.client.post('/calendar/new/project/' + str(project_unassigned.id), {'title': "", 'description': self.project_description, 'start': self.test_start_date, 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.filter(title=self.event_name)
        self.assertFalse(event.exists())
        event.delete()

        #Project does not exist (POST)
        resp = self.client.post('/calendar/new/project/999', {'title': self.event_name, 'description': self.project_description, 'start': self.test_start_date, 'end': self.test_end_date, 'location': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        #Project does not exist (GET)
        resp = self.client.post('/calendar/new/project/999')
        self.assertEqual(404, resp.status_code)

        project_assigned.delete()
        project_unassigned.delete()
        user.delete()

    def test_edit_event(self):

        #init
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user_unassigned = User.objects.create_user('testuser2', 'test@test.de', 'testpw')

        project_assigned = Project(name=self.project_name, description=self.project_description)
        project_assigned.save()
        project_assigned.members.add(user)
        project_assigned.save()

        project_unassigned = Project(name=self.project_name, description=self.project_description)
        project_unassigned.save()
        project_unassigned.members.add(user_unassigned)
        project_unassigned.save()

        event_assigned = Event(title=self.event_name, description=self.project_description, start=self.test_start_date, end=self.test_end_date)
        event_assigned.project = project_assigned
        event_assigned.save()

        event_unassigned = Event(title=self.event_name, description=self.project_description, start=self.test_start_date, end=self.test_end_date)
        event_unassigned.project = project_unassigned
        event_unassigned.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #Open existing and assigned edit/event
        resp = self.client.get('/calendar/edit/' + str(event_assigned.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        #Open existing but not assigned edit/event
        resp = self.client.get('/calendar/edit/' + str(event_unassigned.id))
        self.assertEqual(404, resp.status_code)

        #Open non existing edit/event
        resp = self.client.get('/calendar/edit/999')
        self.assertEqual(404, resp.status_code)

        #Edit existing and assigned Event with title
        resp = self.client.post('/calendar/edit/' + str(event_assigned.id), {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        event = Event.objects.get(id=event_assigned.id)
        self.assertTrue(event.description == "new Description")

        #Edit existing and assigned Event without title
        resp = self.client.post('/calendar/edit/' + str(event_assigned.id), {'title': "", 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        #Edit existing but not assigned edit/event with title
        resp = self.client.post('/calendar/edit/' + str(event_unassigned.id), {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.get(id=event_assigned.id)
        self.assertTrue(event.description == "new Description")

        event = Event.objects.get(id=event_unassigned.id)
        self.assertTrue(event.description == self.project_description)

        #Edit existing but not assigned edit/event without title
        resp = self.client.post('/calendar/edit/' + str(event_unassigned.id), {'title': "", 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.get(id=event_assigned.id)
        self.assertTrue(event.description == "new Description")

        event = Event.objects.get(id=event_unassigned.id)
        self.assertTrue(event.description == self.project_description)

        #Edit non existing Event with Title
        resp = self.client.post('/calendar/edit/999', {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.get(id=event_assigned.id)
        self.assertTrue(event.description == "new Description")

        #Edit non existing Event without Title
        resp = self.client.post('/calendar/edit/999', {'title': "", 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'tags': ""})
        self.assertEqual(404, resp.status_code)

        event = Event.objects.get(id=event_assigned.id)
        self.assertTrue(event.description == "new Description")

        event.delete()
        event_assigned.delete()
        event_unassigned.delete()
        user.delete()
        user_unassigned.delete()
        project_assigned.delete()
        project_unassigned.delete()

    def test_attend_event(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test@test.de', 'testpw')
        user_unassigned = User.objects.create_user('testuser3', 'test@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)
        project.save()

        event = Event(title=self.event_name, description=self.project_description, start=self.test_start_date, end=self.test_end_date)
        event.project = project
        event.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #Assign valid user
        attendees = [user2.username]
        resp = self.client.post('/calendar/edit/' + str(event.id), {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'attendees': attendees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        event_check = Event.objects.get(id=event.id)
        self.assertTrue(user2 in event_check.attendees.all())

        #Assign invalid user only
        attendees = [user_unassigned.username]
        resp = self.client.post('/calendar/edit/' + str(event.id), {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'attendees': attendees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        event_check = Event.objects.get(id=event.id)
        self.assertFalse(user_unassigned in event_check.attendees.all())

        #Assign invalid user and valid user
        attendees = [user_unassigned.username, user2.username]
        resp = self.client.post('/calendar/edit/' + str(event.id), {'title': self.event_name, 'description': "new Description", 'location': "", 'start': self.test_start_date, 'end': self.test_end_date, 'attendees': attendees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        event_check = Event.objects.get(id=event.id)
        self.assertTrue(user2 in event_check.attendees.all())
        self.assertFalse(user_unassigned in event_check.attendees.all())

        event_check.delete()
        event.delete()
        user.delete()
        user2.delete()
        user_unassigned.delete()
        project.delete()