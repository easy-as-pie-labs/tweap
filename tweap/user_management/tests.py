from django.test import TestCase
from django.contrib.auth.models import User


class UserManagementTest(TestCase):
    def test_home(self):
        resp = self.client.get('/users/')
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
