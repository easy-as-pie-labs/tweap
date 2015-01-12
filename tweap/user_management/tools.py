from django.contrib.auth.models import User

bad_passwords = ('123', 'abc',)  # TODO: füllen


def validate_registration_form(username, email, password):
    username = username.strip()
    email = email.strip()
    password = password.strip()
    errors = {}
    if username and email and password:
        if User.objects.filter(username__exact=username).exists():
            errors['username'] = "Benutzername ist nicht verfügbar"  #TODO: Lokalisierung
        if User.objects.filter(email__exact=email).exists():
            errors['email'] = "E-Mail-Adresse wird bereits für einen anderen Account verwendet"  #TODO: Lokalisierung
        if password in bad_passwords:
            errors['password'] = "Lol!"  #TODO: Lokalisierung und Text
    else:
        errors['blank'] = "Es müssen alle Felder ausgefüllt werden"  #TODO: Lokalisierung
    return errors