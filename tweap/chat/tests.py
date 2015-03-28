from django.test import TestCase
from django.contrib.auth.models import User
from user_management.models import Profile, ProfileAddress, PasswordResetToken
from project_management.models import Project
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from chat.models import Conversation


class ConversationProjcetCreation(TestCase):
    def setUp(self):
        user = User.objects.create_user('alice', 'alice@test.de', 'testpw')
        user2 = User.objects.create_user('bob', 'bob@test.de', 'testpw')

    def test_create_alter(self):

        print("__Test Conversation Creation__")

        # site available
        print("Test: site available")
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

        # correct registration
        print("Test: correct registration")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)

        self.client.get('/users/logout/')

        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject1', 'description': 'I am a test project', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exist = Project.objects.filter(name='TestCreateProject1').exists()
        self.assertTrue(project_exist)
        project = Project.objects.get(name='TestCreateProject1')
        self.assertEqual(project.description, 'I am a test project')

        conversation = Conversation.objects.get(name='TestCreateProject1')
        self.assertEqual(conversation.name, 'TestCreateProject1')

        # test if an existing project can be edited
        resp = self.client.get('/projects/edit/' + str(project.id) + '/')
        self.assertEqual(resp.status_code, 200)

        # test if changes are saved
        resp = self.client.post('/projects/edit/' + str(project.id) + '/', {'name': 'new name', 'description': 'new description', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'new name')
        self.assertEqual(project.description, 'new description')

        print('check if conversation was renamed')
        self.assertEqual(Conversation.objects.filter(name='TestCreateProject1').count(), 0)
        self.assertEqual(Conversation.objects.filter(name='new name').count(), 1)

    def test_leave(self):

        print("__Test Delete__")

        # create test user
        print("__Test Conversation Creation__")

        # site available
        print("Test: site available")
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

        # correct registration
        print("Test: correct registration")
        resp = self.client.post('/users/register/', {'username': 'test3', 'email': 'test3@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)

        user = User.objects.get(username='test3')

        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject2', 'description': 'I am a test project', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exist = Project.objects.filter(name='TestCreateProject2').exists()
        self.assertTrue(project_exist)
        project = Project.objects.get(name='TestCreateProject2')
        self.assertEqual(project.description, 'I am a test project')

        conversation = Conversation.objects.get(name='TestCreateProject2')
        self.assertEqual(conversation.name, 'TestCreateProject2')

        print('Test: delete page accessible')
        resp = self.client.get('/users/delete/')
        self.assertEqual(resp.status_code, 200)

        print("Test: delete account, checkbox checked")
        resp = self.client.post('/users/delete/', {'confirm': 'i am sure'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Profile.objects.filter(user=user).count(), 0)

        print("check if conversation deleted")
        self.assertEqual(Conversation.objects.filter(name='TestCreateProject2').count(), 0)

        # site available
        print("Test: site available")
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

        # correct registration
        print("Test: correct registration")
        resp = self.client.post('/users/register/', {'username': 'test3', 'email': 'test3@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post('/users/logout/')

        resp = self.client.post('/users/register/', {'username': 'test4', 'email': 'test4@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)

        user3 = User.objects.get(username='test3')
        user = User.objects.get(username='test4')

        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject2', 'description': 'I am a test project', 'icon': 'fa fa-folder-open-o'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)
        project_exist = Project.objects.filter(name='TestCreateProject2').exists()
        self.assertTrue(project_exist)
        project = Project.objects.get(name='TestCreateProject2')
        self.assertEqual(project.description, 'I am a test project')

        project.members.add(user3)
        project.conversation.members.add(user3)
        project.save()

        conversation = Conversation.objects.get(name='TestCreateProject2')
        self.assertTrue(user in conversation.members.all())
        self.assertTrue(user3 in conversation.members.all())
        self.assertEqual(conversation.name, 'TestCreateProject2')

        print('Test: delete page accessible')
        resp = self.client.get('/users/delete/')
        self.assertEqual(resp.status_code, 200)

        print("Test: delete account, checkbox checked")
        resp = self.client.post('/users/delete/', {'confirm': 'i am sure'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Profile.objects.filter(user=user).count(), 0)

        print("check if conversation still exists, but with a user less")
        conversation = Conversation.objects.get(name='TestCreateProject2')
        self.assertTrue(user3 in conversation.members.all())
        self.assertEqual(conversation.name, 'TestCreateProject2')

