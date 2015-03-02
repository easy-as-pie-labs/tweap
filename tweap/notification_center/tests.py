from django.test import TestCase
import pytz
from project_management.models import Project
from todo.models import Todo
from cal.models import Event
from notification_center.models import Notification, NotificationEvent
from django.contrib.auth.models import User
from datetime import datetime
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect


class ModelTest(TestCase):

    project_name = "Testproject"
    project_description = "Testdescription"
    todo_name = "Testtodo"
    event_name = "Testevent"

    event_todo = "assigned a todo to you"
    event_event = "assigned an event to you"
    event_left = "left your project"

    def test_create_notification(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_todo)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_todo
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2)
        notification.project = project
        notification.target_url = "http://testserver/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        self.assertTrue(notification.receiver == user)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()


class ViewTest(TestCase):
    project_name = "Testproject"
    project_description = "Testdescription"
    todo_name = "Testtodo"
    event_name = "Testevent"

    event_todo = "assigned a todo to you"
    event_event = "assigned an event to you"
    event_left = "left your project"

    dashboard = "/dashboard/"

    def test_view_notification(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_todo)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_todo
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2, project=project, event=notification_event)
        notification.target_url = "http://testserver/todo/edit/"+str(todo.id)
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)


        notification_check = Notification.objects.get(id=notification.id)
        self.assertTrue(user == notification_check.receiver)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # notification delete, by viewing it
        url = '/todo/edit/'+str(todo.id)
        resp = self.client.get('/notifications/view/'+str(notification.id), follow=True)

        notification_check = Notification.objects.filter(id=notification.id).exists()
        self.assertFalse(notification_check)

        # redirects to correct url
        self.assertRedirects(resp, url, 301)

        resp = self.client.get('/notifications/view/'+str(notification.id), follow=True)

        # redirects to dashboard
        self.assertRedirects(resp, self.dashboard, 301)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()


    def test_mark_notification(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_todo)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_todo
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2)
        notification.project = project
        notification.target_url = "http://testserver/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # ajax post
        self.client.post('/notifications/seen/', {'notificationId': notification.id},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # notification deleted
        notification_check = Notification.objects.filter(id=notification.id).exists()
        self.assertFalse(notification_check)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()


    def test_delete_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_todo)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_todo
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2)
        notification.project = project
        notification.target_url = "http://testserver/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # delete todo
        resp = self.client.post('/todo/delete/'+str(todo.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        self.assertFalse(Todo.objects.filter(id=todo.id).exists())
        # notification deleted
        notification_check = Notification.objects.filter(receiver_id=user.id).exists()
        self.assertFalse(notification_check)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def test_edit_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_todo)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_todo
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2)
        notification.project = project
        notification.target_url = "http://testserver/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # edit todoh

        # notification delete, by viewing it
        url = '/todo/edit/'+str(todo.id)
        resp = self.client.get('/notifications/view/'+str(notification.id), follow=True)

        # redirects to correct url
        self.assertRedirects(resp, url, 301)

        # notification deleted
        notification_check = Notification.objects.filter(receiver_id=user.id).exists()
        notification_check2 = Notification.objects.filter(receiver_id=user2.id).exists()
        self.assertFalse(notification_check)
        self.assertFalse(notification_check2)

        self.assertRedirects(resp, notification.target_url, 301)

        assignees = [user2.username]
        self.client.post('/todo/edit/' + str(todo.id), {'title': self.todo_name, 'description': "new Description", 'due_date': "", 'assignees': assignees, 'tags': ""})

        resp = self.client.get('/notifications/view/'+str(notification.id+1), follow=True)

        # redirects to dashboard
        self.assertRedirects(resp, self.dashboard, 301)

        # logout
        self.client.post('users/logout/')

        self.client.post('/users/login/', {'username': 'testuser2', 'password': 'testpw'})

        response = self.client.get('/notifications/view/'+str(notification.id+1), follow=True)
        self.assertRedirects(response, '/todo/edit/'+str(todo.id), 301)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def test_delete_event(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        event = Event(title=self.todo_name, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event.save()
        event.attendees.add(user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # delete event
        resp = self.client.post('/calendar/delete/'+str(event.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        self.assertRedirects(resp, '/projects/'+str(project.id))

        # notification deleted
        notification_check = Notification.objects.filter(receiver_id=user.id).exists()
        notification_check2 = Notification.objects.filter(receiver_id=user2.id).exists()
        self.assertFalse(notification_check)
        self.assertFalse(notification_check2)

        user.delete()
        user2.delete()
        project.delete()
        event.delete()

    def test_edit_event(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        event = Event(title=self.todo_name, project=project, start=datetime.now(pytz.utc), end=datetime.now(pytz.utc))
        event.save()
        event.attendees.add(user)

        try:
            notification_event = NotificationEvent.objects.get(text=self.event_event)
        except:
            notification_event = NotificationEvent()
            notification_event.text = self.event_event
            notification_event.save()

        notification = Notification(receiver=user, trigger_user=user2)
        notification.project = project
        notification.target_url = "http://testserver/calendar/edit/"+str(event.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # edit event
        url = '/calendar/edit/'+str(event.id)
        resp = self.client.get('/notifications/view/'+str(notification.id), follow=True)
        self.assertRedirects(resp, url, 301)

        # notification deleted
        notification_check = Notification.objects.filter(receiver_id=user.id).exists()
        notification_check2 = Notification.objects.filter(receiver_id=user2.id).exists()
        self.assertFalse(notification_check)
        self.assertFalse(notification_check2)

        self.assertRedirects(resp, notification.target_url, 301)

        self.client.post('/calendar/edit/'+str(event.id), {'title': self.todo_name, 'attendees': [user2.username], 'description': "", 'start': event.get_start(), 'end': event.get_end(), 'location': event.location, 'tags': ""})
        notification_check2 = Notification.objects.filter(receiver_id=user2.id).exists()
        self.assertTrue(notification_check2)

        response = self.client.get('/notifications/view/'+str(notification.id+1), follow=True)
        self.assertRedirects(response, self.dashboard, 301)

        # logout
        self.client.post('users/logout/')

        self.client.post('/users/login/', {'username': 'testuser2', 'password': 'testpw'})

        response = self.client.get('/notifications/view/'+str(notification.id+1), follow=True)
        self.assertRedirects(response, '/calendar/edit/'+str(event.id), 301)

        user.delete()
        user2.delete()
        project.delete()
        event.delete()
        notification.delete()

    def test_leave_project(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # leave project
        self.client.post('/projects/leave/', {'project_id': project.id})

        self.assertTrue(Notification.objects.filter(project_id=project.id, receiver_id=user2.id, trigger_user_id=user.id))

        user.delete()
        user2.delete()
        project.delete()