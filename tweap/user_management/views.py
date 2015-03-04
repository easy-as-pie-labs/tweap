from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.models import ProfileAddress, PasswordResetToken
from user_management.tools import validate_registration_form, register_and_login, login, validate_profile_form, delete_user, send_password_reset_link, check_token, validate_reset_password_form
from django.utils.translation import ugettext
from django.contrib.auth.models import User
import json
from user_management.forms import ImageUploadForm

class Register(View):
    """
    View class for registration
    """

    def get(self, request):
        """
        handles get requests
        :param request:
        :return:
        """
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return render(request, 'user_management/register.html', {})

    def post(self, request):
        """
        handles post requests
        :param request:
        :return:
        """
        credentials, errors = validate_registration_form(request.POST)
        if not errors:
            register_and_login(credentials, request)
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        else:
            context = {'error_messages': errors}
            if 'form' not in errors:
                if 'username' not in errors:
                    context['username_field'] = credentials['username']
                if 'email' not in errors:
                    context['email_field'] = credentials['email']
            return render(request, 'user_management/register.html', context)


class Login(View):
    """
    View class for logging in an user
    """
    def get(self, request):
        """
        handles get requests
        :param request:
        :return:
        """
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        context = {'redirect': request.GET.get('next', '')}
        return render(request, 'user_management/login.html', context)

    def post(self, request):
        """
        handles post requests
        :param request:
        :return:
        """
        redirect = request.POST.get('next', '')
        if not redirect:
            redirect = reverse(settings.LOGIN_REDIRECT_URL)
        context = {'redirect': redirect}
        username = str(request.POST.get('username', '')).strip().lower()
        password = str(request.POST.get('password', '')).strip()
        if login(username, password, request):
            return HttpResponseRedirect(redirect)
        else:
            context['error_message'] = ugettext("Login not successful!")
            return render(request, 'user_management/login.html', context)


class Logout(View):
    def get(self, request):
        """
        View function for loging out an user
        :param request:
        :return:
        """
        django_logout(request)
        return HttpResponseRedirect(reverse(settings.LOGIN_URL))


class ViewProfile(View):
    """
    View class for profile viewing
    """
    def get(self, request, user_name):
        """
        handles get requests
        :param request:
        :param user_name: the user name of the profile that should be displayed
        :return:
        """

        user = get_object_or_404(User, username=user_name)
        if user not in request.user.profile.get_connected_users():
            raise Http404
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.address.id)
        except:
            profile_address = None
        context = {'user': user, 'request_user': request.user, 'profile_address': profile_address, 'name': user.profile.get_name()}
        return render(request, 'user_management/profile.html', context)


class EditProfile(View):
    """
    View class for editing a user profile
    """
    def get(self, request):
        """
        handles get requests
        :param request:
        :return:
        """

        user = get_object_or_404(User, id=request.user.id)
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.address.id)
        except:
            profile_address = None


        from user_management.forms import ImageUploadForm
        form = ImageUploadForm() # A empty, unbound form

        image_upload = 'none or success'

        try:
            if request.GET['upload'] == 'failed':
                image_upload = 'fail'
        except:
            pass


        context = {'user': user, 'profile_address': profile_address, 'form': form, 'image_upload': image_upload}
        return render(request, 'user_management/editprofile.html', context)

    def post(self, request):
        """
        handles post requests
        :param request:
        :return:
        """

        errors = validate_profile_form(request.POST, request)

        if errors:
            context = {'error_messages': errors}
            from user_management.forms import ImageUploadForm
            context['form'] = ImageUploadForm
            return render(request, 'user_management/editprofile.html', context)

        '''if 'form' not in errors:
           if 'email' not in errors:
               context['email'] = credentials['email']'''


        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = User.objects.get(id=request.user.id)

        user.email = email

        if password:
            user.set_password(password)

        if request.POST.get('delete_picture', '') == 'delete':
            user.profile.delete_picture()

        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.telephone = phone

        user.save()
        user.profile.save()

        if password:
            login(user.username, password, request)

        street = request.POST.get('street')
        house_number = request.POST.get('housenumber')

        city = request.POST.get('city')
        postal_code = request.POST.get('zip')

        user.profile.address.street = street
        user.profile.address.house_number = house_number
        user.profile.address.postal_code = postal_code
        user.profile.address.city = city
        user.profile.address.save()

        return HttpResponseRedirect(reverse('user_management:profile', kwargs={'user_name': request.user.username}))


class UploadPicture(View):
    def post(self, request):
        """
        view function for uploading a new picture to an user profile
        :param request:
        :return:
        """
        # Handle file upload

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_image = request.FILES['picture']
                user = User.objects.get(id=request.user.id)
                user.profile.add_picture(new_image)

                return HttpResponseRedirect(reverse('user_management:edit_profile'))
            except:
                return HttpResponseRedirect(reverse('user_management:edit_profile') + '?upload=failed')
        else:
            #TODO: instead of redirect, give view info that the upload failed
            return HttpResponseRedirect(reverse('user_management:edit_profile') + '?upload=failed')

class DeleteAccount(View):
    def post(self, request):
        """
        view function for deleting an user account
        :param request:
        :return:
        """
        context = {}
        if request.POST.get('confirm', '') == 'i am sure':
            delete_user(request.user)
            django_logout(request)
            return HttpResponseRedirect(reverse('dashboard:home'))
        else:
            context['error'] = ugettext("Checkbox for confirmation must be checked!")
            return render(request, 'user_management/delete_account.html', context)

    def get(self, request):
        return render(request, 'user_management/delete_account.html', {})


class UserSuggestion(View):
    """
    view function for searching users by user name or email address
    :param request:
    :return: list of users as JSON string
    """
    def get(self, request):
        result = []
        search = request.GET.get('search', '')
        if search:
            users = User.objects.filter(Q(username__istartswith=search) | Q(email__icontains=search))[:5]
            for user in users:
                if user != request.user:
                    result.append(user.username)
        return HttpResponse(json.dumps(result), content_type="application/json")


class LostPassword(View):
    """
    view class for requesting link via email to reset user password
    """
    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return render(request, 'user_management/lost_password.html', {})

    def post(self, request):
        username = request.POST.get('username', '').strip().lower()
        if username:
            result = send_password_reset_link(username, request.build_absolute_uri(reverse('user_management:reset_password')))
            if result == "user_error":
                context = {'error_message': ugettext("Sorry, we couldn't find that user!")}
            if result == "mail_error":
                context = {'error_message': ugettext("Sorry, we couldn't send the email. That's our fault. Please try again later!")}
            if result == "success":
                context = {'success_message': ugettext("We've send you a link to reset your password.")}
        else:
            context = {'error_message': ugettext("Username must not be empty!")}

        return render(request, 'user_management/lost_password.html', context)


class ResetPassword(View):
    """
    view class for password reset
    """
    def get(self, request, reset_token=None):
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        context = {'reset_token': reset_token}
        if not check_token(reset_token):
            context['wrong_token'] = ugettext("This link is not valid.")
        return render(request, 'user_management/reset_password.html', context)

    def post(self, request, reset_token):
        user = check_token(reset_token)
        if not user:
            return render(request, 'user_management/reset_password.html', {'wrong_token': ugettext("This link is not valid.")})
        error, password = validate_reset_password_form(request.POST, user)
        if error:
            return render(request, 'user_management/reset_password.html', {'reset_token': reset_token, 'error_message': error})
        else:
            user.set_password(password)
            user.save()
            PasswordResetToken.objects.get(token=reset_token).delete()
            if login(user.username, password, request):
                return redirect(reverse(settings.LOGIN_REDIRECT_URL))
            else:
                return render(request, 'user_management/reset_password.html', {'reset_token': reset_token, 'error_message': ugettext("There was an error during login!")})




