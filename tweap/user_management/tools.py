from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
import re

bad_passwords = ('123', 'abc',)  # TODO: füllen


def validate_registration_form(form):

    errors = {}
    credentials = {}

    if 'username' in form and 'email' in form and 'password' in form:

        credentials['username'] = form['username'].strip().lower()
        credentials['email'] = form['email'].strip().lower()
        credentials['password'] = str(form['password']).strip()

        if credentials['username'] and credentials['email'] and credentials['password']:

            if User.objects.filter(username=credentials['username']).exists():
                errors['username'] = "Benutzername ist nicht verfügbar"  # TODO: Lokalisierung
            if not re.match("[^@]+@[^@]+\.[^@]+", credentials['email']):
                errors['email'] = "Die eingegebene E-Mail-Adresse ist keine gültige E-Mail-Adresse"  # TODO: Lokalisierung
            if User.objects.filter(email=credentials['email']).exists():
                errors['email'] = "E-Mail-Adresse wird bereits für einen anderen Account verwendet"  # TODO: Lokalisierung
            if credentials['password'] in bad_passwords:
                errors['password'] = "Das gewählte Passwort ist zu unsicher!"  # TODO: Lokalisierung

        else:
            errors['blank'] = "Es müssen alle Felder ausgefüllt werden"  # TODO: Lokalisierung

    else:
        errors['form'] = "Es ist ein Fehler bei der Übertragung des Formulars aufgetreten"  # TODO: Lokalisierung

    return credentials, errors


def register_and_login(credentials, request):
    User.objects.create_user(credentials['username'], credentials['email'], credentials['password'])
    login(credentials['username'], credentials['password'], request)


def login(username, password, request):
    user = authenticate(username=username, password=password)
    if user is None:
        return False
    django_login(request, user)
    return True