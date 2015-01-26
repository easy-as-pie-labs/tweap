from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import logout as django_logout
from user_management.models import ProfileAddress, PostalCode
from user_management.tools import validate_registration_form, register_and_login, login, cleanup_postal_code
from django.utils.translation import ugettext
from django.contrib.auth.models import User


class Register(View):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return render(request, 'user_management/register.html', {})

    def post(self, request):
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
    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        context = {'redirect': request.GET.get('next', '')}
        return render(request, 'user_management/login.html', context)

    def post(self, request):
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
    django_logout(request)
    context = {'redirect': request.GET.get('next', '')}
    return render(request, 'user_management/logout.html', context)


class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            welcome_message = ugettext("Home! Hello ") + request.user.username
        else:
            welcome_message = ugettext("Home! Hello Guest!")
        return HttpResponse(welcome_message)


class ViewProfile(View):
    def get(self, request, user_name=None):
        if user_name is None:
            user_name = request.user.username
        user = get_object_or_404(User, username=user_name)
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.address.id)
            postal_code = PostalCode.objects.get(id=profile_address.postal_code.id)
        except:
            profile_address = None
            postal_code = None
        context = {'user': user, 'profile_address': profile_address, 'postal_code': postal_code}
        return render(request, 'user_management/profile.html', context)


class EditProfile(View):
    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        try:
            profile_address = ProfileAddress.objects.get(id=user.profile.address.id)
            postal_code = PostalCode.objects.get(id=profile_address.postal_code.id)
        except:
            profile_address = None
            postal_code = None


        from user_management.forms import ImageUploadForm
        form = ImageUploadForm() # A empty, unbound form
        context = {'user': user, 'profile_address': profile_address, 'postal_code': postal_code, 'form': form}
        return render(request, 'user_management/editprofile.html', context)

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_repeat = request.POST.get('passwordrepeat')

        user = User.objects.get(id=request.user.id)

        user_check = None
        try:
            user_check = User.objects.get(email=email)
        except:
            pass

        if user_check is not None:
            # TODO: error => email already in use
            pass
        else:
            user.email = email


        picture = request.FILES['docfile']
        user.profile.picture.save(picture.name, picture)
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.telephone = phone

        if password != "" and password is not None:
            if password == password_repeat:
                user.set_password(password)
            else:
                #TODO: error => passwords not identical
                pass

        user.save()
        user.profile.save()

        street = request.POST.get('street')
        house_number = request.POST.get('housenumber')

        city = request.POST.get('city')
        zip = request.POST.get('zip')

        # if one of the address fields is empty, ignore the address change for the time being
        if street == "" or house_number == "" or city == "" or zip == "":
            return HttpResponseRedirect(reverse('user_management:profile'))

        try:
            postal_code = PostalCode.objects.get(postal_code=zip)
        except:
            postal_code = PostalCode.create(zip, city)
            postal_code.save()

        if user.profile.address is None:
            address = ProfileAddress.create(street, house_number, postal_code)
            address.save()
            user.profile.address = address
            user.profile.save()
        else:
            user.profile.address.street = street
            user.profile.address.house_number = house_number

            # check if old postal code is not in use anymore and can be deleted
            old_postal = user.profile.address.postal_code

            user.profile.address.postal_code = postal_code
            user.profile.address.save()

            #delete old postal code if it isn't needed anymore
            cleanup_postal_code(old_postal)

        return HttpResponseRedirect(reverse('user_management:profile'))

def upload_picture(request):
    from user_management.forms import ImageUploadForm
    # Handle file upload
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = request.FILES['picture']
            user = User.objects.get(id=request.user.id)
            user.profile.add_picture(new_image)

            return HttpResponseRedirect(reverse('user_management:edit_profile'))
