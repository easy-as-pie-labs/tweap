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

    def test_create_todo(self):
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

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #User is assigned to project (GET)
        resp = self.client.get('/todo/new/project/' + str(project_assigned.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        #User is assgined to project and Title is not empty
        resp = self.client.post('/todo/new/project/' + str(project_assigned.id), {'title': self.todo_name, 'description': "", 'due_date': "", 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo = Todo.objects.filter(title=self.todo_name)
        self.assertTrue(todo.exists())
        todo.delete()

        #User is assigned to project but Title is empty
        resp = self.client.post('/todo/new/project/' + str(project_assigned.id), {'title': "", 'description': "", 'due_date': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        todo = Todo.objects.filter(title=self.todo_name)
        self.assertFalse(todo.exists())
        todo.delete()

        #User is unassigned to project (GET)
        resp = self.client.get('/todo/new/project/' + str(project_unassigned.id))
        self.assertEqual(404, resp.status_code)

        #User is unassigned to project and Title is not empty
        resp = self.client.post('/todo/new/project/' + str(project_unassigned.id), {'title': self.todo_name, 'description': "", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.filter(title=self.todo_name)
        self.assertFalse(todo.exists())
        todo.delete()

        #User is unassgined to project and Title is empty
        resp = self.client.post('/todo/new/project/' + str(project_unassigned.id), {'title': "", 'description': "", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.filter(title=self.todo_name)
        self.assertFalse(todo.exists())
        todo.delete()

        #Project does not exist (POST)
        resp = self.client.post('/todo/new/project/999', {'title': self.todo_name, 'description': "", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        #Project dies not exist (GET)
        resp = self.client.get('/todo/new/project/999')
        self.assertEqual(404, resp.status_code)

        project_assigned.delete()
        project_unassigned.delete()
        user.delete()
        user_unassigned.delete()

    def test_create_edit_todo(self):

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

        todo_assigned = Todo(title=self.todo_name, description=self.project_description)
        todo_assigned.project = project_assigned
        todo_assigned.save()

        todo_unassigned = Todo(title=self.todo_name, description=self.project_description)
        todo_unassigned.project = project_unassigned
        todo_unassigned.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #Open existing and assigned edit/todoh
        resp = self.client.get('/todo/edit/' + str(todo_assigned.id))
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)

        #Open existing but not assigned edit/todoh
        resp = self.client.get('/todo/edit/' + str(todo_unassigned.id))
        self.assertEqual(404, resp.status_code)

        #Open non existing edit/todoh
        resp = self.client.get('/todo/edit/999')
        self.assertEqual(404, resp.status_code)

        #Edit existing and assigned todoh with title
        resp = self.client.post('/todo/edit/' + str(todo_assigned.id), {'title': self.todo_name, 'description': "new Description", 'due_date': "", 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo = Todo.objects.get(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")

        #Edit existing and assigned todoh without title
        resp = self.client.post('/todo/edit/' + str(todo_assigned.id), {'title': "", 'description': "newer", 'due_date': "", 'tags': ""})
        self.assertEqual(200, resp.status_code)
        self.assertTrue(type(resp) is HttpResponse)
        self.assertTrue(resp.context['error_messages'])

        '''todo = Todo.objects.filter(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")'''

        #Edit existing but not assigned edit/todoh with title
        resp = self.client.post('/todo/edit/' + str(todo_unassigned.id), {'title': self.todo_name, 'description': "newer Description", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.get(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")

        #Edit existing but not assigned edit/todoh without title
        resp = self.client.post('/todo/edit/' + str(todo_unassigned.id), {'title': "", 'description': "newest Description", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.get(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")

        #Edit non existing todoh with title
        resp = self.client.post('/todo/edit/999', {'title': self.todo_name, 'description': "latest Description", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.get(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")

        #Edit non existing todoh without title
        resp = self.client.post('/todo/edit/999', {'title': "", 'description': "later Description", 'due_date': "", 'tags': ""})
        self.assertEqual(404, resp.status_code)

        todo = Todo.objects.get(id=todo_assigned.id)
        self.assertTrue(todo.description == "new Description")

        todo.delete()
        todo_assigned.delete()
        todo_unassigned.delete()
        user.delete()
        user_unassigned.delete()
        project_assigned.delete()
        project_unassigned.delete()

    def test_assign_todo(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test@test.de', 'testpw')
        user_unassigned = User.objects.create_user('testuser3', 'test@test.de', 'testpw')

        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        project.members.add(user)
        project.members.add(user2)
        project.save()

        todo = Todo(title=self.todo_name, description=self.project_description)
        todo.project = project
        todo.save()

        #Login
        self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpw'})

        #Assign valid user
        assignees = [user2.username]
        resp = self.client.post('/todo/edit/' + str(todo.id), {'title': self.todo_name, 'description': "new Description", 'due_date': "", 'assignees': assignees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo_check = Todo.objects.get(id=todo.id)
        self.assertTrue(user2 in todo_check.assignees.all())

        #Assign invalid user only
        assignees = [user_unassigned.username]
        resp = self.client.post('/todo/edit/' + str(todo.id), {'title': self.todo_name, 'description': "new Description", 'due_date': "", 'assignees': assignees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo_check = Todo.objects.get(id=todo.id)
        self.assertFalse(user_unassigned in todo_check.assignees.all())

        #Assign invalid user and valid user
        assignees = [user_unassigned.username, user2.username]
        resp = self.client.post('/todo/edit/' + str(todo.id), {'title': self.todo_name, 'description': "new Description", 'due_date': "", 'assignees': assignees, 'tags': ""})
        self.assertEqual(302, resp.status_code)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        todo_check = Todo.objects.get(id=todo.id)
        self.assertTrue(user2 in todo_check.assignees.all())
        self.assertFalse(user_unassigned in todo_check.assignees.all())

        todo_check.delete()
        todo.delete()
        user.delete()
        user2.delete()
        user_unassigned.delete()
        project.delete()

    def test_due_date_todo(self):
        pass

    def test_complete_todo(self):
        pass

    def test_delete_todo(self):
        pass