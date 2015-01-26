from django.db import models
from django.contrib.auth.models import User
# default charfield length 50 chars, just to be safe


class PostalCode(models.Model):
    # international postal codes may have dashes and letters
    postal_code = models.CharField(max_length=50)

    # the longest city name has 97 letters (in New Zealand)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.postal_code + " " + self.city

    @classmethod
    def create(cls, postal_code, city):
        postal_code_object = cls(postal_code=postal_code, city=city)
        return postal_code_object


class ProfileAddress(models.Model):
    street = models.CharField(max_length=100)

    # could be something like 50A
    house_number = models.CharField(max_length=50)

    postal_code = models.ForeignKey(PostalCode)

    def __str__(self):
        return self.street + " " + self.house_number + ", " + str(self.postal_code)

    @classmethod
    def create(cls, street, house_number, postal_code):
        profile_address = cls(street=street, house_number=house_number, postal_code=postal_code)
        return profile_address


class Profile(models.Model):
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # leading zeros etc
    telephone = models.CharField(max_length=50, null=True, blank=True)
    address = models.ForeignKey(ProfileAddress, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    def add_picture(self, picture):
        self.picture = picture
        self.save()
        #self.picture.url = "123.png"
        #self.save()

    def __str__(self):
        if self.first_name is None and self.last_name is None:
            return str(self.user.id) + ": " + str(self.user.username)
        return str(self.user.id) + ": " + str(self.first_name) + " " + str(self.last_name)

    @classmethod
    def create(cls, user):
        profile = cls(user=user)
        return profile