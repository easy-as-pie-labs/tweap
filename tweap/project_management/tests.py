from django.test import TestCase
from project_management.models import Project, Invitation
from project_management.tools import invite_users
from django.contrib.auth.models import User
import json


class ModelTest(TestCase):

    project_name = "Testproject"
    project_description = "Testdescription"

    def test_project_model_members_and_leave(self):
        user = User.objects.create_user('testuser', 'test@test.de', 'testpw')
        user2 = User.objects.create_user('testuser2', 'test2@test.de', 'testpw')
        project = Project(name=self.project_name, description=self.project_description)
        project.save()
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


class ViewsTest(TestCase):

    def setup_login(self):
        User.objects.create_user('user', 'user@test.de', 'testpw')
        self.client.post('/users/login/', {'username': 'user', 'password': 'testpw'})

    def test_project_create_edit(self):
        self.setup_login()

        # test if page is available
        resp = self.client.get('/projects/new/')
        self.assertEqual(resp.status_code, 200)

        # test if validation works
        resp = self.client.post('/projects/new/', {})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['error_messages'])

        # test if project with name only can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject'})
        self.assertEqual(resp.status_code, 302)
        project_exist = Project.objects.filter(name='TestCreateproject').exists()
        self.assertTrue(project_exist)

        # test if project with name and description can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject2', 'description': 'I am a test project'})
        self.assertEqual(resp.status_code, 302)
        project_exist = Project.objects.filter(name='TestCreateproject2').exists()
        self.assertTrue(project_exist)
        project = Project.objects.get(name='TestCreateproject2')
        self.assertEqual(project.description, 'I am a test project')

        # test if a non existing project retuns 404
        resp = self.client.get('/projects/edit/9999/')
        self.assertEqual(resp.status_code, 404)

        # test if an existing project can be edited
        resp = self.client.get('/projects/edit/' + str(project.id) + '/')
        self.assertEqual(resp.status_code, 200)

        # test if changes are saved
        resp = self.client.post('/projects/edit/' + str(project.id) + '/', {'name': 'new name', 'description': 'new description'})
        self.assertEqual(resp.status_code, 302)
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'new name')
        self.assertEqual(project.description, 'new description')

    def test_project_view(self):
        self.setup_login()

        # test if project with name only can be created
        resp = self.client.post('/projects/new/', {'name': 'TestCreateProject'})
        self.assertEqual(resp.status_code, 302)
        project_exists = Project.objects.filter(name='TestCreateproject').exists()
        self.assertTrue(project_exists)
        project = Project.objects.get(name='TestCreateproject')

        resp = self.client.get('/projects/' + str(project.id))
        self.assertEqual(resp.status_code, 200)


        pass

    def test_view_all(self):
        pass

    def test_view_invites(self):
        pass

    def test_leave(self):
        pass

    def test_invitation_handler(self):
        pass




