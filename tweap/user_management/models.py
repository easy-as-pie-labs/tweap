from django.db import models
from django.contrib.auth.models import User
from os.path import splitext
from project_management.models import Project
import random
import hashlib
from django.utils.translation import ugettext
# default charfield length 50 chars, just to be safe


# generates filename from user id + random seed md5 hashed
def get_filename(instance, filename):
    """
    returns a filename for a profile picture
    :param instance: the profile object
    :param filename: the original file name on the client system
    :return: a md5 hash of the user id + random int in range 1000-9999
    """
    filename, file_extension = splitext(filename)
    filename = hashlib.md5(str(str(instance.user.id) + str(random.randint(1000, 9999))).encode('utf-8')).hexdigest()
    return 'profile_pictures/' + filename + file_extension


class ProfileAddress(models.Model):
    """
    Model for a profile address
    """
    street = models.CharField(max_length=100, null=True, blank=True)

    # could be something like 50A
    house_number = models.CharField(max_length=50, null=True, blank=True)

    # international postal codes may have dashes and letters
    postal_code = models.CharField(max_length=50, null=True, blank=True)

    # the longest city name has 97 letters (in New Zealand)
    city = models.CharField(max_length=100, null=True, blank=True)

    # TODO: can someone please improve this?
    def __str__(self):
        string = ""
        if self.city is not None and self.city != "":
            string += self.city
        if self.postal_code is not None and self.postal_code != "":
            string = self.postal_code + " " + string
        if self.house_number is not None and self.house_number != "":
            if self.street is not None and self.street != "":
                if string != "":
                    # street and house number are set and at least city or zip code
                    # myStreet 23, city / myStreet 23, 24941 / myStreet 23, 24941 Flensburg
                    return self.street + " " + self.house_number + ", " + string
                else:
                    # street and house number are set nut neither city nor zip code
                    # myStreet 23
                    return self.street + " " + self.house_number
            else:
                if string != "":
                    # street isn't set, but city or zip
                    # Number 23, Flensburg
                    return ugettext("Number") + ": " + self.house_number + ", " + string
                else:
                    # street isn't set, neither are city or zip
                    # Number 23
                    return ugettext("Number") + ": " + self.house_number
        elif self.street is not None and self.street != "":
            # house number not set, but street and city or zip
            # myStreet, Flensburg
            if string != "":
                return self.street + ", " + string
            else:
                # city zip not set
                # myStreet
                return self.street
        else:
            # house_number and street not set
            # city or zip might be set
            # Flensburg / 24941 Flensburg / 24941 / ""
            return string

    @classmethod
    def create(cls, street, house_number, postal_code, city):
        """
        creates an instance of this class
        :param street: the street name
        :param house_number: the house number
        :param postal_code: reference to a postal code object
        :return: the created instance
        """
        profile_address = cls(street=street, house_number=house_number, postal_code=postal_code, city=city)
        return profile_address


class Profile(models.Model):
    """
    Model for the profile of an user
    """
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # leading zeros etc
    telephone = models.CharField(max_length=50, null=True, blank=True)
    address = models.ForeignKey(ProfileAddress, null=True, blank=True)
    picture = models.ImageField(upload_to=get_filename, null=True, blank=True)

    def add_picture(self, picture):
        """
        adds a picture to the profile
        :param picture: the filename of the picture on the system
        :return:
        """
        self.picture.delete(save=False)
        self.picture = picture
        self.save()

    def get_connected_users(self):
        """
        creates a list of all users, the current user is connected with via projects
        :return: the list of connected users
        """
        connected_users = [self.user]
        projects = Project.objects.filter(members=self.user.id)
        for project in projects:
            members = project.members.all()
            for member in members:
                if member not in connected_users:
                    connected_users.append(member)
        return connected_users

    def __str__(self):
        if self.first_name is None and self.last_name is None:
            return str(self.user.id) + ": " + str(self.user.username)
        return str(self.user.id) + ": " + str(self.first_name) + " " + str(self.last_name)

    @classmethod
    def create(cls, user):
        """
        creates an instance of this class
        :param user: the user the profile will be created for
        :return: the created instance
        """
        profile = cls(user=user)
        return profile








