from django.contrib.auth.models import User
import re

bad_passwords = ('123', 'abc',)  # TODO: füllen


def validate_registration_form(username, email, password):
    username = username.strip()
    email = email.strip()
    password = password.strip()
    errors = {}
    if username and email and password:
        if User.objects.filter(username__iexact=username).exists():
            errors['username'] = "Benutzername ist nicht verfügbar"  #TODO: Lokalisierung
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            errors['email'] = "Die eingegebene E-Mail-Adresse ist keine gültige E-Mail-Adresse"  #TODO: Lokalisierung
        if User.objects.filter(email__iexact=email).exists():
            errors['email'] = "E-Mail-Adresse wird bereits für einen anderen Account verwendet"  #TODO: Lokalisierung
        if password in bad_passwords:
            errors['password'] = "Lol!"  #TODO: Lokalisierung und Text
    else:
        errors['blank'] = "Es müssen alle Felder ausgefüllt werden"  #TODO: Lokalisierung
    return errors