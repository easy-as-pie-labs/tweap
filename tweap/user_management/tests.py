from django.test import TestCase
from django.contrib.auth.models import User


class UserManagementTest(TestCase):
    def test_home(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, 200)

    def test_register(self):

        # site available
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

        # correct registration
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'test'})
        self.assertEqual(resp.status_code, 302)

        # username and email already in use
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test@test.de', 'password': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertTrue('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        # username already in use
        resp = self.client.post('/users/register/', {'username': 'test', 'email': 'test2@test.de', 'password': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])

        # username is an email address
        resp = self.client.post('/users/register/', {'username': 'test3@test.de', 'email': 'test2@test.de', 'password': 'test'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.context['error_messages'])
        self.assertFalse('email' in resp.context['error_messages'])
        self.assertFalse('password' in resp.context['error_messages'])
        self.assertFalse('blank' in resp.context['error_messages'])
        self.assertFalse('form' in resp.context['error_messages'])


        '''
        Alles korrekt -> Redirect
        Name + Mail belegt -> check
        Name belegt -> check
        Name ist Email -> check
        Mail belegt ->
        Mail keine gültige Mail ->
        Bad Password ->
        Passwort == Username ->
        Passwort == Email ->
        leerer Name ->
        leere Mail ->
        leeres PW ->
        Name nicht übermittelt ->
        Mail nicht übermittelt ->
        PW nicht übermittelt ->
        '''

