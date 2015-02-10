from django.test import TestCase
from project_management.models import Project, Invitation, Tag
from todo.models import Todo
from django.contrib.auth.models import User
import datetime
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed


class ModelTest(TestCase):

    project_name = "Testproject"
    project_description = "Testdescription"
    todo_name = "Testtodo"

    def test_create_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertTrue(Todo.get_open_for_project(project).exists())
        self.assertFalse(Todo.get_closed_for_project(project).exists())
        self.assertFalse(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertFalse(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertFalse(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertFalse(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertFalse(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def test_assign_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertTrue(Todo.get_open_for_project(project).exists())
        self.assertFalse(Todo.get_closed_for_project(project).exists())
        self.assertTrue(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertTrue(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertFalse(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertFalse(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertFalse(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def test_assign_todo_due_today(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)
        todo.due_date = datetime.date.today()
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertTrue(Todo.get_open_for_project(project).exists())
        self.assertFalse(Todo.get_closed_for_project(project).exists())
        self.assertTrue(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertTrue(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertFalse(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertFalse(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertTrue(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def test_assign_todo_overdue(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)
        todo.due_date = datetime.date.today() - datetime.timedelta(days=1)
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertTrue(Todo.get_open_for_project(project).exists())
        self.assertFalse(Todo.get_closed_for_project(project).exists())
        self.assertTrue(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertTrue(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertFalse(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertTrue(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertFalse(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def test_assign_todo_due_this_week(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)
        todo.due_date = datetime.date.today() + datetime.timedelta(days=2)
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertTrue(Todo.get_open_for_project(project).exists())
        self.assertFalse(Todo.get_closed_for_project(project).exists())
        self.assertTrue(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertTrue(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertFalse(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertFalse(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertFalse(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertTrue(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def test_assign_todo_closed(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()

        self.assertEqual(str(project), self.project_name)

        project.members.add(user)
        project.members.add(user2)
        # test if users are in project now
        self.assertTrue(user in project.members.all())
        self.assertTrue(user2 in project.members.all())

        todo = Todo(title=self.todo_name, project=project)
        todo.save()
        todo.assignees.add(user)
        todo.due_date = datetime.date.today() + datetime.timedelta(days=2)
        todo.done = True
        todo.save()

        self.assertTrue(Todo.get_all_for_project(project).exists())
        self.assertFalse(Todo.get_open_for_project(project).exists())
        self.assertTrue(Todo.get_closed_for_project(project).exists())
        self.assertTrue(Todo.get_all_for_user(user).exists())
        self.assertFalse(Todo.get_all_for_user(user2).exists())
        self.assertFalse(Todo.get_open_for_user(user).exists())
        self.assertFalse(Todo.get_open_for_user(user2).exists())
        self.assertTrue(Todo.get_closed_for_user(user).exists())
        self.assertFalse(Todo.get_closed_for_user(user2).exists())
        self.assertFalse(Todo.get_overdue_for_user(user).exists())
        self.assertFalse(Todo.get_overdue_for_user(user2).exists())
        self.assertFalse(Todo.get_due_today_for_user(user).exists())
        self.assertFalse(Todo.get_due_today_for_user(user2).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user).exists())
        self.assertFalse(Todo.get_due_this_week_for_user(user2).exists())

        # cleanup
        todo.delete()
        project.delete()
        user.delete()
        user2.delete()


class ViewsTest(TestCase):
    project_name = "Testproject"
    project_description = "Testdescription"
    todo_name = "Testtodo"

    def create_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        resp = self.client.get('/todo/new/project/' + str(project.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/todo/new/project/' + str(project.id), {'name': self.todo_name})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo = Todo.objects.get(name=self.todo_name)
        self.assertTrue(todo.exists())

        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def create_edit_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        resp = self.client.get('/todo/new/project/' + str(project.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/todo/new/project/' + str(project.id), {'name': self.todo_name})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo = Todo.objects.get(name=self.todo_name)
        self.assertTrue(todo.exists())

        resp = self.client.get('/todo/edit/' + str(todo.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/todo/edit/' + str(todo.id), {'name': 'another todo'})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo = Todo.objects.get(name='another todo')
        self.assertTrue(todo.exists())

        todo.delete()
        project.delete()
        user.delete()
        user2.delete()

    def assign_todo(self):
        pass

    def due_date_todo(self):
        pass

    def complete_todo(self):
        pass

    def delete_todo(self):
        pass