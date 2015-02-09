from django.test import TestCase
from project_management.models import Project, Invitation, Tag
from project_management.tools import invite_users, get_tags
from django.contrib.auth.models import User
import json
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException


class ModelTest(TestCase):

    project_name = "Testproject"
    project_description = "Testdescription"

    def test_project_model_members_and_leave(self):
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

        project.leave(user2)
        project_exists = Project.objects.filter(id=project.id).exists()
        # test if user2 is removed from project and project still exists
        self.assertTrue(project_exists)
        self.assertTrue(user in project.members.all())
        self.assertFalse(user2 in project.members.all())

        project.leave(user)
        project_exists = Project.objects.filter(id=project.id).exists()
        # test if leave of last user deletes the project
        self.assertFalse(project_exists)

        # cleanup
        user.delete()
        user2.delete()

    def test_invitation_model_get_for_users(self):
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        invitation = Invitation(user=user, project=project)
        invitation.save()

        self.assertEqual(str(invitation), user.username + ' invited to ' + self.project_name)
        # test if invitation is returned for the user via the method get_for_user()
        self.assertTrue(invitation in Invitation.get_for_user(user))
        invitation.delete()

        # cleanup
        user.delete()

    def test_invitation_model_accept(self):
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        invitation = Invitation(user=user, project=project)
        invitation.save()
        invitation_exists = Invitation.objects.filter(id=invitation.id).exists()
        # test if invitation exists
        self.assertTrue(invitation_exists)
        invitation.accept()
        invitation_exists = Invitation.objects.filter(id=invitation.id).exists()
        # test if user is now member of the project and invitation was deleted
        self.assertTrue(user in project.members.all())
        self.assertFalse(invitation_exists)

        # cleanup
        user.delete()

    def test_invitation_model_reject(self):
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        invitation = Invitation(user=user, project=project)
        invitation.save()
        invitation_exists = Invitation.objects.filter(id=invitation.id).exists()
        # test if invitation exists
        self.assertTrue(invitation_exists)
        invitation.reject()
        invitation_exists = Invitation.objects.filter(id=invitation.id).exists()
        # test if user is not member of the project and invitation was deleted
        self.assertFalse(user in project.members.all())
        self.assertFalse(invitation_exists)

        # cleanup
        user.delete()


class ToolsTest(TestCase):

    def test_invite_users(self):
        project = Project(name="Testprojekt")
        project.save()

        user1 = User.objects.create_user('user1', 'user1@test.de', 'testpw')
        user2 = User.objects.create_user('user2', 'user2@test.de', 'testpw')
        user3 = User.objects.create_user('user3', 'user3@test.de', 'testpw')
        # test with username and email
        user_string = ['user1', 'user2@test.de', 'test']
        user_string = json.dumps(user_string)
        invite_users(user_string, project)
        # test if the both users are invited
        self.assertTrue(Invitation.objects.filter(user=user1, project=project).exists())
        self.assertTrue(Invitation.objects.filter(user=user2, project=project).exists())
        self.assertFalse(Invitation.objects.filter(user=user3, project=project).exists())

        #cleanup
        user1.delete()
        user2.delete()
        user3.delete()

    def test_get_tags(self):
        project = Project(name="Testprojekt")
        project.save()
        tag = Tag(name="testtag1", project=project)
        tag.save()

        #test if only testtag1 exists
        self.assertTrue(Tag.objects.filter(project=project, name="testtag1").exists())
        self.assertFalse(Tag.objects.filter(project=project, name="testtag2").exists())
        self.assertFalse(Tag.objects.filter(project=project, name="testtag3").exists())

        tag_string = ['testttag1', 'testtag2', 'testtag3']
        tag_string = json.dumps(tag_string)
        tags = get_tags(tag_string, project)

        #test if return list contains 3 Tags
        self.assertEquals(len(tags), 3)
        self.assertIsInstance(tags[0], Tag)

        #test that all 3 testtags exists now
        self.assertTrue(Tag.objects.filter(project=project, name="testtag1").exists())
        self.assertTrue(Tag.objects.filter(project=project, name="testtag2").exists())
        self.assertTrue(Tag.objects.filter(project=project, name="testtag3").exists())


class ViewsTest(TestCase):

    def setup_login(self):
        User.objects.create_user('user', 'user@test.de', 'testpw')
        self.client.post('/users/login/', {'username': 'user', 'password': 'testpw'})

    def test_project_create_edit(self):
        self.setup_login()

        # test if page is available
        resp = self.client.get('/projects/new/')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('error_messages' in resp.context)

        # test if validation works
        resp = self.client.post('/projects/new/', {})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['error_messages'])

        # test if project with name only can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exist = Project.objects.filter(name='TestCreateProject').exists()
        self.assertTrue(project_exist)

        # test if project with name and description can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject2', 'description': 'I am a test project', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exist = Project.objects.filter(name='TestCreateProject2').exists()
        self.assertTrue(project_exist)
        project = Project.objects.get(name='TestCreateProject2')
        self.assertEqual(project.description, 'I am a test project')

        # test if a non existing project retuns 404
        resp = self.client.get('/projects/edit/9999/')
        self.assertEqual(resp.status_code, 404)

        # test if an existing project can be edited
        resp = self.client.get('/projects/edit/' + str(project.id) + '/')
        self.assertEqual(resp.status_code, 200)

        # test if changes are saved
        resp = self.client.post('/projects/edit/' + str(project.id) + '/', {'name': 'new name', 'description': 'new description', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'new name')
        self.assertEqual(project.description, 'new description')

    def test_project_view(self):
        self.setup_login()

        # test if project with name only can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exists = Project.objects.filter(name='TestCreateProject').exists()
        self.assertTrue(project_exists)
        project = Project.objects.get(name='TestCreateProject')

        print('test: acces own project')
        resp = self.client.get('/projects/' + str(project.id))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/projects/' + str(project.id))
        self.assertTrue(type(resp) is HttpResponseNotAllowed)

        print('test non-existent project')
        resp = self.client.get('/projects/1337')
        self.assertEqual(resp.status_code, 404)

        self.client.get('/users/logout/')

        print('test: access \'own\' project when not logged in')
        resp = self.client.get('/projects/' + str(project.id))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)

        User.objects.create_user('anotheruser', 'anotheruser@test.de', 'testpw')
        self.client.post('/users/login/', {'username': 'anotheruser', 'password': 'testpw'})

        print('test: someone else\'s project')
        resp = self.client.get('/projects/' + str(project.id))
        self.assertEqual(resp.status_code, 404)

    def test_view_all(self):
        # TODO: renew tests
        pass

    def test_view_invites(self):
        # TODO: renew tests
        pass

    def test_leave(self):
        pass

    def test_invitation_handler(self):
        pass
