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

    PostalCode_id = models.ForeignKey(PostalCode)

    def __str__(self):
        return self.street + " " + self.house_number + ", " + str(self.PostalCode_id)


class Profile(models.Model):
    user_id = models.OneToOneField(User)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    # leading zeros etc
    telephone = models.CharField(max_length=50, blank=True)
    address_id = models.ForeignKey(ProfileAddress, null=True, blank=True)
    picture = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name