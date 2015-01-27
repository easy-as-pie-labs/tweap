from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from user_management.models import Profile
from django.utils.translation import ugettext
from user_management.models import ProfileAddress, PostalCode
import re

bad_passwords = ('123', 'abc',)  # TODO: füllen


def validate_registration_form(form):
    """
    validates the registration form
    :param form: the registration form received via POST
    :return: a list of errors and the cleaned credentials
    """
    errors = {}
    credentials = {}

    if 'username' in form and 'email' in form and 'password' in form:

        credentials['username'] = str(form['username']).strip().lower()
        credentials['email'] = form['email'].strip().lower()
        credentials['password'] = str(form['password']).strip()

        if credentials['username'] and credentials['email'] and credentials['password']:

            if User.objects.filter(username=credentials['username']).exists():
                errors['username'] = ugettext("The username isn't available")
            if not re.match("^[A-Za-z0-9-]+$", credentials['username']):
                errors['username'] = ugettext("The username can only contain letters and numbers")
            if not re.match("[^@]+@[^@]+\.[^@]+", credentials['email']):
                errors['email'] = ugettext("The email address isn't valid")
            if User.objects.filter(email=credentials['email']).exists():
                errors['email'] = ugettext("The email address is already in use")
            if credentials['password'] in bad_passwords or \
               credentials['password'] == credentials['username'] or \
               credentials['password'] == credentials['email']:
                errors['password'] = ugettext("The password is super weak")

        else:
            errors['blank'] = ugettext("All fields must be filled out")

    else:
        errors['form'] = ugettext("An error occurred during form transfer")

    return credentials, errors


def register_and_login(credentials, request):
    """
    creates an user and performs log in for that new user
    :param credentials: the credentials (username, email, password) for the new user
    :param request: the request object for log in
    :return:
    """
    user = User.objects.create_user(credentials['username'], credentials['email'], credentials['password'])
    profile = Profile.create(user)
    profile.save()
    login(credentials['username'], credentials['password'], request)


def login(username, password, request):
    """
    logs in an user
    :param username: the username
    :param password: the password
    :param request: the request
    :return: True if log in was succesfull, otherwise False
    """
    user = authenticate(username=username, password=password)
    if user is None:
        return False
    django_login(request, user)
    return True


def cleanup_postal_code(postal_code):
    """
    deletes a postal code if it is not in use anymore
    :param postal_code: PostalCode object
    :return:
    """
    ref_count = ProfileAddress.objects.filter(postal_code=postal_code).count()

    if ref_count == 0:
        postal_code.delete()