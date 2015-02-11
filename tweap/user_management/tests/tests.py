from django.test import TestCase
from django.contrib.auth.models import User
from user_management.models import Profile, ProfileAddress
from project_management.models import Project
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


class UserManagementTest(TestCase):
    def test_home(self):

        print("__Test Dashboard__")
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)

        #register
        resp = self.client.post('/users/register/', {'username': 'myusername', 'email': 'me@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        #login
        resp = self.client.post('/users/login/', {'username': 'myusername', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/dashboard/')
        self.assertTrue(type(resp) is HttpResponseNotAllowed)

    def test_register(self):

        print("__Test Regisration__")

        # site available
        print("Test: site available")
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

        # correct registration
        print("Test: correct registration")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 302)
        # self.assertEqual(resp.context['username'], 'test')  # TODO: anpassen auf Dashboard

        self.client.get('/users/logout/')

        resp = self.client.post('/dashboard/')
        self.assertTrue(type(resp) is HttpResponseNotAllowed)

        # username and email already in use
        print("Test: username and email already in use")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'testpw'})

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username_field' in resp.context)
        self.assertFalse('email_field' in resp.context)

        # username already in use
        print("Test: username already in use")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username_field' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email_field'])

        # username contains non alphanumerical symbols
        print("Test: username contains non alphanumerical symbols")
        resp = self.client.post('/users/register/', {'username': 'tes@t!', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username_field' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email_field'])

        # email already in use
        print("Test: email already in use")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username_field'])
        self.assertFalse('email_field' in resp.context)

        # email format is not valid
        print("Test: email format is not valid")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'testtest.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username_field'])
        self.assertFalse('email_field' in resp.context)

        # password is in bad password list
        print("Test: password is in bad password list")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'abc'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username_field'])
        self.assertEqual('test2@test.de', resp.context['email_field'])

        # password equals username
        print("Test: password equals username")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'test2'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username_field'])
        self.assertEqual('test2@test.de', resp.context['email_field'])

        # password equals email
        print("Test: password equals email")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'test2@test.de'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertTrue('username_field' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email_field'])

        # username is blank
        print("Test: username is blank")
        resp = self.client.post('/users/register/', {'username': '', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertTrue('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        # email is blank
        print("Test: email is blank")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': '', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertTrue('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        # password is blank
        print("Test: password is blank")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': ' '})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertTrue('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        # username field is missing in POST
        print("Test: username field is missing in POST")
        resp = self.client.post('/users/register/', {'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertTrue('form' in resp.context['error_messages'])
        self.assertFalse('username_field' in resp.context)
        self.assertFalse('email_field' in resp.context)

    def test_login(self):

        print("__Test Login__")

        # site available
        print("Test: site available")
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, 200)

        # create test user
        User.objects.create_user('correctusername', 'logintest@test.de', 'correct_password')

        # correct login
        print("Test: correct login")
        resp = self.client.post('/users/login/', {'username': 'correctusername', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        # self.assertEqual(resp.context['username'], 'test')  # TODO: anpassen auf Dashboard

        # incorrect password
        print("Test: incorrect password")
        resp = self.client.post('/users/login/', {'username': 'correctusername', 'password': 'incorrect_password'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

        # incorrect username
        print("Test: incorrect username")
        resp = self.client.post('/users/login/', {'username': 'incorrectusername', 'password': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

        # incorrect username
        print("Test: blank fields")
        resp = self.client.post('/users/login/', {'username': '', 'password': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

    def test_edit_profile(self):

        print("__Test Edit__")
        # create test user
        resp = self.client.post('/users/register/', {'username': 'myusername', 'email': 'me@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post('/users/register/', {'username': 'anotherdude', 'email': 'used@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        # correct login
        print("Test: correct login")
        resp = self.client.post('/users/login/', {'username': 'myusername', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print('profile is viewable')
        resp = self.client.get('/users/profile/myusername/')
        self.assertEqual(resp.status_code, 200)

        print('unknown person\'s profile is not viewable')
        resp = self.client.get('/users/profile/anotherdude')
        self.assertEqual(resp.status_code, 301)

        print('site is editable')
        resp = self.client.get('/users/editprofile/')
        self.assertEqual(resp.status_code, 200)

        print('profile was edited succesfully')
        resp = self.client.post('/users/editprofile/', {'email': 'new@test.de', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswort', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 302)

        print('profile was edited succesfully, complete address')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': '', 'first_name': '', 'last_name': '', 'phone': '', 'city': 'a city', 'zip': '24941', 'street': 'a street', 'housenumber': '23'})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='myusername')
        self.assertEqual(str(user.profile), str(user.id) + ': ' + 'myusername')
        self.assertEqual(str(user.profile.address), 'a street 23, 24941 a city')

        print('profile was edited succesfully, no city, no zip code')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': '', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': 'a street', 'housenumber': '23'})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='myusername')
        self.assertEqual(str(user.profile), str(user.id) + ': ' + 'myusername')
        self.assertEqual(str(user.profile.address), 'a street 23  ')

        print('profile was edited succesfully, no street, no housenumber')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': '', 'first_name': '', 'last_name': '', 'phone': '', 'city': 'a city', 'zip': '24941', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='myusername')
        self.assertEqual(str(user.profile), str(user.id) + ': ' + 'myusername')
        self.assertEqual(str(user.profile.address), '  24941 a city')

        print('profile was edited succesfully, no house number')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': '', 'first_name': '', 'last_name': '', 'phone': '', 'city': 'a city', 'zip': '24941', 'street': 'some street', 'housenumber': ''})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='myusername')
        self.assertEqual(str(user.profile), str(user.id) + ': ' + 'myusername')
        self.assertEqual(str(user.profile.address), 'some street, 24941 a city')

        print('profile was edited succesfully, password not changed')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': '', 'first_name': 'my', 'last_name': 'username', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='myusername')
        self.assertEqual(str(user.profile), str(user.id) + ': ' + 'my username')
        self.assertEqual(str(user.profile.address), '   ')

        print('email address already in use')
        resp = self.client.post('/users/editprofile/', {'email': 'used@test.de', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswort', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('email address blank')
        resp = self.client.post('/users/editprofile/', {'email': '', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswort', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('email address invalid')
        resp = self.client.post('/users/editprofile/', {'email': 'thisisnotanemailaddress', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswort', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('passwords do not match')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswortNichtGleich', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('passwords do not match, second is blank')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'meinPasswort', 'passwordrepeat': '', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('passwords do not match, first is blank')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': 'eshrherher', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('password cannot be username')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'myusername', 'passwordrepeat': 'my_username', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('password cannot be username, email already taken')
        resp = self.client.post('/users/editprofile/', {'email': 'used@test.de', 'password': 'myusername', 'passwordrepeat': 'my_username', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('form has been tempered with')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'myusername', 'passwordrepeat': 'my_username', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('form' in resp.context['error_messages'])

    def test_delete_account(self):

        print("__Test Delete__")

        # create test user
        resp = self.client.post('/users/register/', {'username': 'usertobedeleted', 'email': 'usertobedeleted@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(username='usertobedeleted')

        address_id = user.profile.address.id

        project = Project.objects.create()
        project.members.add(user)
        project.save()

        resp = self.client.post('/users/login/', {'username': 'usertobedeleted', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print("Test: delete account, checkbox not checked")
        resp = self.client.post('/users/delete/', {})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.filter(username='usertobedeleted').count(), 1)

        print('Test: delete page accessible')
        resp = self.client.get('/users/delete/')
        self.assertEqual(resp.status_code, 200)

        print("Test: delete account, checkbox checked")
        resp = self.client.post('/users/delete/', {'confirm': 'i am sure'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.filter(username='usertobedeleted').count(), 0)
        self.assertEqual(Profile.objects.filter(user=user).count(), 0)
        self.assertEqual(ProfileAddress.objects.filter(id=address_id).count(), 0)
        self.assertEqual(Project.objects.filter(members=user).count(), 0)
        self.assertEqual(Project.objects.filter(id=project.id).count(), 0)

        resp = self.client.post('/users/register/', {'username': 'usertobedeleted', 'email': 'usertobedeleted@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post('/users/register/', {'username': 'anotheruser', 'email': 'anotheruser@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        user = User.objects.get(username='usertobedeleted')
        user2 = User.objects.get(username='anotheruser')

        address_id = user.profile.address.id

        project = Project.objects.create()
        project.members.add(user)
        project.members.add(user2)
        project.save()

        project2 = Project.objects.create()
        project2.members.add(user)
        project2.save()

        # correct login
        print("Test: correct login")
        resp = self.client.post('/users/login/', {'username': 'usertobedeleted', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print("Test: delete account, checkbox checked")
        resp = self.client.post('/users/delete/', {'confirm': 'i am sure'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.filter(username='usertobedeleted').count(), 0)
        self.assertEqual(Profile.objects.filter(user=user).count(), 0)
        self.assertEqual(Project.objects.filter(id=project.id).count(), 1)
        self.assertEqual(ProfileAddress.objects.filter(id=address_id).count(), 0)
        self.assertEqual(Project.objects.filter(members=user).count(), 0)
        self.assertEqual(Project.objects.filter(id=project2.id).count(), 0)


class ViewTest(TestCase):
    def test_view_access_denied(self):

        print("__Test Access denied__")

        # register a user to view
        resp = self.client.post('/users/register/', {'username': 'theirusername', 'email': 'them@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        #register
        resp = self.client.post('/users/register/', {'username': 'myusername', 'email': 'me@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        #login
        resp = self.client.post('/users/login/', {'username': 'myusername', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print('test: register redirect when user is already logged in')
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 302)

        print('test: login redirect when user is already logged in')
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, 302)

        print('test: try to view a profile of someone the user is not connected to')
        resp = self.client.get('/users/profile/theirusername/')
        self.assertEqual(resp.status_code, 404)

        print('test: try to view a profile of someone who doesn\'t exist')
        resp = self.client.get('/users/profile/notauser/')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/users/logout/')
        self.assertEqual(resp.status_code, 200)

        print('test: try to edit profile when not logged in')
        resp = self.client.get('/users/editprofile/')
        self.assertEqual(resp.status_code, 302)

        print('test: try to view \'own\' profile when not logged in')
        resp = self.client.get('/users/profile/myusername/')
        self.assertEqual(resp.status_code, 302)

    def test_view_accessibility(self):

        print("__Test Accessibility__")

        resp = self.client.post('/users/register/', {'username': 'connecteduser', 'email': 'anotheruser@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post('/users/register/', {'username': 'thirdguy', 'email': 'yetanotheruser@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post('/users/register/', {'username': 'activeuser', 'email': 'usertobedeleted@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        user = User.objects.get(username='activeuser')
        user2 = User.objects.get(username='connecteduser')

        project = Project.objects.create()
        project.members.add(user)
        project.members.add(user2)
        project.save()

        #login
        resp = self.client.post('/users/login/', {'username': 'activeuser', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print('test: try to view own profile when logeed in')
        resp = self.client.get('/users/profile/activeuser/')
        self.assertEqual(resp.status_code, 200)

        print('test: try to view a profile of someone the user is connected to')
        resp = self.client.get('/users/profile/connecteduser/')
        self.assertEqual(resp.status_code, 200)

        print('test: try to edit own profile')
        resp = self.client.get('/users/editprofile/')
        self.assertEqual(resp.status_code, 200)

        print('test: try to edit the profile of someone the user is connected to')
        resp = self.client.get('/users/editprofile/connecteduser')
        self.assertEqual(resp.status_code, 404)

        print('test: try to edit the profile of someone the user is not connected to')
        resp = self.client.get('/users/editprofile/thirdguy')
        self.assertEqual(resp.status_code, 404)

    def test_upload_image(self):

        print("__Test image upload__")

        resp = self.client.post('/users/register/', {'username': 'imageuploadtest', 'email': 'imageupload@test.de', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print('test: no picture uploaded')
        picture = User.objects.get(username='imageuploadtest').profile.picture
        self.assertEqual(picture, '')
        # TODO: Upload here the image

