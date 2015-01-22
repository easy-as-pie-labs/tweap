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


class ProfileAddress(models.Model):
    street = models.CharField(max_length=100)

    # could be something like 50A
    house_number = models.CharField(max_length=50)

    postalCode = models.ForeignKey(PostalCode)

    def __str__(self):
        return self.street + " " + self.house_number + ", " + str(self.postalCode)


class Profile(models.Model):
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # leading zeros etc
    telephone = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(ProfileAddress, null=True, blank=True)
    picture = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.first_name == None and self.last_name == None:
            return str(self.user.id) + ": " + str(self.user.username)
        return str(self.user.id) + ": " + str(self.first_name) + " " + str(self.last_name)

    @classmethod
    def create(cls, user):
        profile = cls(user=user)
        return profile