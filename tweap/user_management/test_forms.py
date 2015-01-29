from django.test import TestCase
from django.contrib.auth.models import User
from user_management.models import Profile, ProfileAddress
from project_management.models import Project


class UserManagementTest(TestCase):
    def test_home(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)

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

        # username and email already in use
        print("Test: username and email already in use")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username' in resp.context)
        self.assertFalse('email' in resp.context)

        # username already in use
        print("Test: username already in use")
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email'])

        # username contains non alphanumerical symbols
        print("Test: username contains non alphanumerical symbols")
        resp = self.client.post('/users/register/', {'username': 'tes@t!', 'email': 'test2@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertFalse('username' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email'])

        # email already in use
        print("Test: email already in use")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test@test.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username'])
        self.assertFalse('email' in resp.context)

        # email format is not valid
        print("Test: email format is not valid")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'testtest.de', 'password': 'testpw'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username'])
        self.assertFalse('email' in resp.context)

        # password is in bad password list
        print("Test: password is in bad password list")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'abc'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username'])
        self.assertEqual('test2@test.de', resp.context['email'])

        # password equals username
        print("Test: password equals username")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'test2'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertEqual('test2', resp.context['username'])
        self.assertEqual('test2@test.de', resp.context['email'])

        # password equals email
        print("Test: password equals email")
        resp = self.client.post('/users/register/', {'username': 'test2', 'email': 'test2@test.de', 'password': 'test2@test.de'})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])
        self.assertTrue('username' in resp.context)
        self.assertEqual('test2@test.de', resp.context['email'])

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
        self.assertFalse('username' in resp.context)
        self.assertFalse('email' in resp.context)

    def test_login(self):

        print("__Test Login__")

        # site available
        print("Test: site available")
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, 200)

        # create test user
        User.objects.create_user('correct_username', 'logintest@test.de', 'correct_password')

        # correct login
        print("Test: correct login")
        resp = self.client.post('/users/login/', {'username': 'correct_username', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)
        # self.assertEqual(resp.context['username'], 'test')  # TODO: anpassen auf Dashboard

        # incorrect password
        print("Test: incorrect password")
        resp = self.client.post('/users/login/', {'username': 'correct_username', 'password': 'incorrect_password'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

        # incorrect username
        print("Test: incorrect username")
        resp = self.client.post('/users/login/', {'username': 'incorrect_username', 'password': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

        # incorrect username
        print("Test: blank fields")
        resp = self.client.post('/users/login/', {'username': '', 'password': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('error_message' in resp.context)

    def test_edit_profile(self):
        # create test user
        user = User.objects.create_user('my_username', 'me@test.de', 'correct_password')
        profile = Profile.create(user)
        profile.save()
        User.objects.create_user('antoher_dude', 'used@test.de', 'correct_password')

        # correct login
        print("Test: correct login")
        resp = self.client.post('/users/login/', {'username': 'my_username', 'password': 'correct_password'})
        self.assertEqual(resp.status_code, 302)

        print('profile is viewable')
        resp = self.client.get('/users/profile/')
        self.assertEqual(resp.status_code, 200)

        print('site is editable')
        resp = self.client.get('/users/editprofile/')
        self.assertEqual(resp.status_code, 200)

        print('profile was edited succesfully')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'meinPasswort', 'passwordrepeat': 'meinPasswort'})
        self.assertEqual(resp.status_code, 200)

        print('profile was edited succesfully, password not changed')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': '', 'passwordrepeat': ''})
        self.assertEqual(resp.status_code, 200)

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
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'my_username', 'passwordrepeat': 'my_username', 'first_name': '', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        print('form has been tempered with')
        resp = self.client.post('/users/editprofile/', {'email': 'me@test.de', 'password': 'my_username', 'passwordrepeat': 'my_username', 'last_name': '', 'phone': '', 'city': '', 'zip': '', 'street': '', 'housenumber': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertTrue('form' in resp.context['error_messages'])

    def delete_account(self):
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

        '''
        print("Test: delete account, checkbox not checked")
        resp = self.client.post('/users/delete/', {})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.filter(username='user_to_be_deleted').count(), 1)
        '''
        print("Test: delete account, checkbox checked")
        resp = self.client.post('/users/delete/', {'confirm': 'i am sure'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(User.objects.filter(username='usertobedeleted').count(), 0)
        self.assertEqual(Profile.objects.filter(user=user).count(), 0)
        self.assertEqual(ProfileAddress.objects.filter(id=address_id).count(), 0)
        self.assertEqual(Project.objects.filter(members=user).count(), 0)

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