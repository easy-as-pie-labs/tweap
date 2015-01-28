from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.models import ProfileAddress
from user_management.tools import validate_registration_form, register_and_login, login, validate_profile_form
from django.utils.translation import ugettext
from django.contrib.auth.models import User
from project_management.models import Project as ProjectModel, Invitation
import json


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
                    context['username'] = credentials['username']
                if 'email' not in errors:
                    context['email'] = credentials['email']
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


def logout(request):
    """
    View function for loging out an user
    :param request:
    :return:
    """
    django_logout(request)
    context = {'redirect': request.GET.get('next', '')}
    return render(request, 'user_management/logout.html', context)


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
        context = {'user': user, 'request_user': request.user, 'profile_address': profile_address}
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
        context = {'user': user, 'profile_address': profile_address, 'form': form}
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
        password_repeat = request.POST.get('passwordrepeat')

        user = User.objects.get(id=request.user.id)

        user.email = email

        if password:
            user.set_password(password)

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


        if user.profile.address is None:
            address = ProfileAddress.create(street, house_number, postal_code, city)
            address.save()
            user.profile.address = address
            user.profile.save()
        else:
            user.profile.address.street = street
            user.profile.address.house_number = house_number
            user.profile.address.postal_code = postal_code
            user.profile.address.city = city
            user.profile.address.save()


        return HttpResponseRedirect(reverse('user_management:profile', kwargs={'user_name': request.user.username}))


def upload_picture(request):
    """
    view function for uploading a new picture to an user profile
    :param request:
    :return:
    """
    from user_management.forms import ImageUploadForm
    # Handle file upload
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = request.FILES['picture']
            user = User.objects.get(id=request.user.id)
            user.profile.add_picture(new_image)

            return HttpResponseRedirect(reverse('user_management:edit_profile'))


def user_suggestion(request):
    """
    view function for searching users by user name or email address
    :param request:
    :return: list of users as JSON string
    """
    if request.method == 'GET':
        result = []
        search = request.GET.get('search', '')
        if len(search) > 1:
            users = User.objects.filter(Q(username__icontains=search) | Q(email__icontains=search))[:5]
            for user in users:
                if user != request.user:
                    result.append(user.username)
        return HttpResponse(json.dumps(result), content_type="application/json")
