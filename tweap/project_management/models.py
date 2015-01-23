from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name
