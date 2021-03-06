from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from user_management.models import Profile, PasswordResetToken
from project_management.models import Project, Invitation
from django.utils.translation import ugettext
from user_management.models import ProfileAddress
from django.db import IntegrityError
from django.core.mail import send_mail
import re
import hashlib
import random
import datetime
import pytz


bad_passwords = ('123', 'abc',)  # TODO: füllen
bad_usernames = ['alice', 'bob', 'all', 'me']


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

            if User.objects.filter(username=credentials['username']).exists() or \
               credentials['username'] in bad_usernames:
                 errors['username'] = ugettext("The username isn't available")
            if not re.match("^[A-Za-z0-9]+$", credentials['username']):
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

def validate_profile_form(form, request):

    errors = {}
    credentials = {}

    if 'email' in form and\
            'password' in form and\
            'passwordrepeat' in form and\
            'first_name' in form and\
            'last_name' in form and\
            'phone' in form and\
            'city' in form and\
            'zip' in form and\
            'street' in form and\
            'housenumber' in form:

        credentials['email'] = form['email'].strip().lower()
        credentials['password'] = str(form['password'].strip())
        credentials['passwordrepeat'] = str(form['passwordrepeat'].strip())

        if credentials['password'] != credentials['passwordrepeat']:
            errors['password'] = ugettext("Passwords do not match!")
        if credentials['password'] and credentials['passwordrepeat']:
            if credentials['password'] in bad_passwords or credentials['password'] == request.user.username or\
                            credentials['password'] == credentials['email']:
                errors['password'] = ugettext("The password is super weak")

        if not re.match("[^@]+@[^@]+\.[^@]+", credentials['email']):
            errors['email'] = ugettext("The email address isn't valid")
        else:
            if User.objects.filter(email=credentials['email']).exists():
                if User.objects.get(email=credentials['email']) != request.user:
                    errors['email'] = ugettext("This email is already in use")
    else:
        errors['form'] = ugettext("An error occurred during form transfer")

    return errors


def register_and_login(credentials, request):
    """
    creates an user and performs log in for that new user
    :param credentials: the credentials (username, email, password) for the new user
    :param request: the request object for log in
    :return:
    """
    user = User.objects.create_user(credentials['username'], credentials['email'], credentials['password'])
    profile = Profile.create(user)
    address = ProfileAddress.create("", "", "", "")
    address.save()
    profile.address = address
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


def delete_user(user):
    """
    removes an user account
    :param user:
    :return:
    """
    # remove user from projects and delete invitations of the user
    projects = Project.objects.filter(members=user)
    for project in projects:
        project.leave(user)
    invitations = Invitation.objects.filter(user=user)
    for invitation in invitations:
        invitation.delete()

    # delete user and log out
    user.profile.address.delete()
    user.delete()

def send_password_reset_link(user, url):
    """
    creates a reset password token for an user, stores it in db and sends it via email
    :param user: the user who gets the reset token
    :return: True when created and sended token, False when user doesn't exists
    """
    try:
        user = User.objects.get(username=user)
        # if old tokens are in the database delete them
        PasswordResetToken.objects.filter(user=user).delete()
        # TODO: think about much more secure hash generation
        reset_token = hashlib.md5((str(datetime.datetime.now()) + str(random.randint(0, 9999999999999999999))).encode('utf-8')).hexdigest()
        PasswordResetToken(user=user, token=reset_token).save()
        email_text = ugettext("You requested a password reset link, so here it is!\n""Click the following link to reset your password:\n") +\
            url + reset_token + ugettext("\n\nHappy tweaping!")
        send_mail(ugettext('Set your new tweap password'), email_text, 'tweap@easy-as-pie.de', [user.email], fail_silently=True)
        return "success"
    except User.DoesNotExist:
        return "user_error"
    except IntegrityError:
        # if the same hash is present in db, try again
        send_password_reset_link(user)
    except OSError:
        return "mail_error"

def check_token(reset_token):
    """
    checks an password reset token for existence and
    :param reset_token: token to check
    :return: user of token when token is valid, False when not
    """
    try:
        token = PasswordResetToken.objects.get(token=reset_token)
        if token.timestamp > (datetime.datetime.now(pytz.utc) - datetime.timedelta(days=(1))):
            return token.user
        else:
            token.delete()
            return False
    except PasswordResetToken.DoesNotExist:
        return False

def validate_reset_password_form(form, user):
    """
    checks password guidelines for new password
    :param form: the form data
    :param user: the user whos changing password
    :return: error message and if no errors, the new password
    """
    error = ""
    new_password = ""
    if 'password' in form and 'password' in form:
        password = str(form['password']).strip()
        password2 = str(form['password2']).strip()
        if password and password2:
            if password != password2:
                error = ugettext("Passwords do not match!")
            elif password in bad_passwords or \
               password == user.username or \
               password == user.email:
                error = ugettext("The password is super weak!")
            else:
                new_password = password
        else:
            error = ugettext("All fields must be filled out!")
    else:
        error = ugettext("An error occurred during form transfer.")
    return error, new_password
