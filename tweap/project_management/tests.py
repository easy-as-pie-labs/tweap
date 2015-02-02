from django.test import TestCase
from project_management.models import Project, Invitation
from project_management.tools import invite_users
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
        self.setup_login()

        print('test: access own projects')
        resp = self.client.get('/projects/all/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/projects/all/')
        self.assertTrue(type(resp) is HttpResponseNotAllowed)

        self.client.get('/users/logout/')

        print('test: access projects when not logged in')
        resp = self.client.get('/projects/all/')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)

    def test_view_invites(self):
        self.setup_login()

        print('test: access invites')
        resp = self.client.get('/projects/invites/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(type(resp) is HttpResponse)

        resp = self.client.post('/projects/invites/')
        self.assertTrue(type(resp) is HttpResponseNotAllowed)

        self.client.get('/users/logout/')

        print('test: access invites when not logged in')
        resp = self.client.get('/projects/invites/')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(type(resp) is HttpResponseRedirect)

    def test_leave(self):
        pass

    def test_invitation_handler(self):
        pass


class SeleniumTest(TestCase):
    browser = None

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.email = '@projectmanagement.de'
        self.password = 'datPassword'
        self.timeout = 2

    def register(self, username, email, password):
        self.browser.get('http://127.0.0.1:8000/users/register/')
        self.assertTrue('Tweap' in self.browser.title)

        elem = self.browser.find_element_by_name('username')
        elem.send_keys(username)

        elem = self.browser.find_element_by_name('email')
        elem.send_keys(email)

        elem = self.browser.find_element_by_name('password')
        elem.send_keys(password + Keys.RETURN)

    def login(self, username, password):
        self.browser.get('http://127.0.0.1:8000/users/login/')

        elem = self.browser.find_element_by_name('username')
        elem.send_keys(username)

        elem = self.browser.find_element_by_name('password')
        elem.send_keys(password + Keys.RETURN)

    def logout(self):
        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_logout_link'))
        elem.click()

    def delete_account(self):
        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_profile_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('make_changes'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('delete_account'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('confirm'))
        elem.click()

        elem = self.browser.find_element_by_name('delete_account')
        elem.click()

    ''' ----------------------------------------------------------------------------
    ------------------------ actual tests start here -------------------------------
    ---------------------------------------------------------------------------- '''
    def test_new_project(self):
        print('ui_test: create project')
        username = 'testnewproject'

        self.register(username, username + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.delete_account()
        self.browser.close()

    def test_view_invite(self):
        print('ui_test: view project')
        initiator = 'testnewproject2'
        receiver = 'testviewinvite'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('acceptInvitation'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('edit_project'))
        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('leave_project'))

        self.delete_account()

        self.login(initiator, self.password)
        self.delete_account()
        self.browser.close()

    def test_reject_invite(self):
        print('ui_test: reject project invite')
        initiator = 'testnewproject'
        receiver = 'testrejectinvite'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('rejectInvitation'))
        elem.click()

        self.delete_account()

        self.login(initiator, self.password)
        self.delete_account()
        self.browser.close()

    def test_accept_invite(self):
        print('ui_test: accept project invite')
        initiator = 'testnewproject'
        receiver = 'testacceptinvite'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('acceptInvitation'))
        elem.click()

        self.delete_account()

        self.login(initiator, self.password)
        self.delete_account()
        self.browser.close()

    def test_view_project(self):
        print('ui_test: view project')
        initiator = 'testnewprojectview'
        receiver = 'testviewproject'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('acceptInvitation'))
        elem.click()

        self.logout()

        self.login(initiator, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_projects_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_class_name('list-group-item'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_class_name('panel-heading'))
        elem.click()

        self.delete_account()

        self.login(receiver, self.password)
        self.delete_account()
        self.browser.close()

    def test_edit_project(self):
        print('ui_test: edit project')
        initiator = 'testnewproject3'
        receiver = 'testeditproject'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('acceptInvitation'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('edit_project'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('description'))
        elem.send_keys(', yeah!')

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.delete_account()

        self.login(initiator, self.password)
        self.delete_account()
        self.browser.close()

    def test_leave_project(self):
        print('ui_test: leave project')
        initiator = 'testnewproject4'
        receiver = 'testleaveproject'

        self.register(receiver, receiver + self.email, self.password)
        self.logout()

        self.register(initiator, initiator + self.email, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_new_link'))
        elem.click()

        elem = self.browser.find_element_by_name('name')
        elem.send_keys('a great project')

        elem = self.browser.find_element_by_name('description')
        elem.send_keys('a great project description')

        elem = self.browser.find_element_by_id('users')
        elem.send_keys(receiver)

        elem = self.browser.find_element_by_name('create_save')
        elem.click()

        self.logout()

        self.login(receiver, self.password)

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('navbar_invites_link'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('acceptInvitation'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('leave_project'))
        elem.click()

        WebDriverWait(self.browser, 30, 1, (ElementNotVisibleException)).until(lambda x: x.find_element_by_name('leave_project_confirm').is_displayed())

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_name('leave_project_confirm'))
        elem.click()

        elem = WebDriverWait(self.browser, self.timeout).until(lambda x: x.find_element_by_id('your_projects_heading'))

        self.delete_account()

        self.login(initiator, self.password)
        self.delete_account()
        self.browser.close()
