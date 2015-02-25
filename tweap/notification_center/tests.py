from django.test import TestCase
import pytz
from project_management.models import Project
from todo.models import Todo
from cal.models import Event
from notification_center.models import Notification, NotificationEvent
from django.contrib.auth.models import User
from datetime import datetime
from django.http.response import HttpResponse, HttpResponseRedirect


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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/todo/edit/"+str(todo.id)
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

    dashboard = "/dashboard"

    def view_notification(self): #TODO FAILING TEST
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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        resp = self.client.get('/notifications/view/'+str(notification.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        # notification deleted
        self.assertFalse(notification.receiver == user)
        url = '/todo/edit/'+str(todo.id)

        # redirected to correct url
        self.assertRedirects(resp, url)


        resp = self.client.get('/notifications/view/'+str(notification.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        # redirected to dashboard
        self.assertRedirects(resp, self.dashboard)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def mark_notification(self): #TODO FAILING TEST
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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/todo/edit/"+str(todo.id)
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
        self.assertFalse(notification.receiver == user)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def delete_todo(self): #TODO FAILING TEST
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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # delete todoh
        resp = self.client.post('todo/delete'+str(todo.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        # notification deleted
        self.assertFalse(notification.receiver == user)

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def edit_todo(self): #TODO FAILING TEST
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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/todo/edit/"+str(todo.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # edit todoh
        resp = self.client.get('notifications/view'+str(notification.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        # notification deleted
        self.assertFalse(notification.receiver == user)
        self.assertFalse(notification.receiver == user2)

        self.assertRedirects(resp, notification.target_url)

        self.client.post('/todo/edit/'+str(todo.id), {'title': self.todo_name, 'assignees': ['testuser2']})

        response = self.client.get('/notifications/view/2')
        self.assertRedirects(response, self.dashboard)

        # logout
        self.client.post('users/logout/')

        self.client.post('/users/login/', {'username': 'testuser2', 'password': 'testpw'})

        response = self.client.get('/notifications/view/2')
        self.assertRedirects(response, '/todo/edit/'+str(todo.id))

        user.delete()
        user2.delete()
        project.delete()
        todo.delete()
        notification.delete()

    def delete_event(self): #TODO FAILING TEST
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

        # notification created
        self.assertTrue(Notification.objects.filter(receiver_id=user2.id))

        user.delete()
        user2.delete()
        project.delete()
        event.delete()

    def edit_event(self): #TODO FAILING TEST
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
        notification.target_url = "http://dev.tweap.easy-as-pie.de/calendar/edit/"+str(event.id)
        notification.event = notification_event
        notification.save()

        # Has notification
        self.assertTrue(notification.receiver == user)

        # Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        # edit event
        resp = self.client.get('notifications/view'+str(notification.id))
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        # notification deleted
        self.assertFalse(notification.receiver == user)
        self.assertFalse(notification.receiver == user2)

        self.assertRedirects(resp, notification.target_url)

        self.client.post('/calendar/edit/'+str(event.id), {'title': self.todo_name, 'assignees': ['testuser2']})

        response = self.client.get('/notifications/view/2')
        self.assertRedirects(response, self.dashboard)

        # logout
        self.client.post('users/logout/')

        self.client.post('/users/login/', {'username': 'testuser2', 'password': 'testpw'})

        response = self.client.get('/notifications/view/2')
        self.assertRedirects(response, '/calendar/edit/'+str(event.id))

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