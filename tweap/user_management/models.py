from django.db import models
from django.contrib.auth.models import User
from os.path import splitext
from project_management.models import Project, Invitation
from todo.models import Todo
from cal.models import Event
import random
import hashlib
import datetime
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


def create_tutorial_project(user):
    """
    create a tutorial project for a newly registered user
    :param user:
    :return:
    """
    #2. create a new project, add one demo user as member, one as invited
    #3. create at least four todos (one overdue, one due today, one due tomorrow, one already checked off)
    #4 create two calendar entries (one due today, one in two days)

    # get tutorial users alice and bob
    alice = User.objects.get(username='alice')
    bob = User.objects.get(username='bob')

    # create tutorial project, add user and alice
    tutorial = Project(name="Tutorial", icon="fa fa-recycle", description="This is just a Tutorial, so that you can get the hang of tweap!")
    tutorial.save()
    tutorial.members.add(user)
    tutorial.members.add(alice)
    tutorial.save()

    # invite bob
    Invitation(user=bob, project=tutorial).save()

    # create todos
    todo = Todo(title="This is an overdue todo!", project=tutorial)
    todo.save()
    todo.description = "You should really get going on this one!"
    todo.due_date = datetime.date.today() - datetime.timedelta(days=1)
    todo.assignees.add(user)
    todo.assignees.add(alice)
    todo.save()

    todo = Todo(title="This is due today!", project=tutorial)
    todo.save()
    todo.description = "You planned to do this today, so why don't you?"
    todo.due_date = datetime.date.today()
    todo.assignees.add(user)
    todo.save()

    todo = Todo(title="This is due tomorrow!", project=tutorial)
    todo.save()
    todo.description = "You still got some time left..."
    todo.due_date = datetime.date.today() + datetime.timedelta(days=1)
    todo.assignees.add(user)
    todo.save()

    todo = Todo(title="Alice already completed this todo!", project=tutorial)
    todo.save()
    todo.description = "Yay!"
    todo.due_date = datetime.date.today() - datetime.timedelta(days=3)
    todo.done = True
    todo.assignees.add(alice)
    todo.save()

    # create events
    event = Event(title="It's happening later today!", project=tutorial)
    event.start = datetime.datetime.today() + datetime.timedelta(hours=1)
    event.end = datetime.datetime.today() + datetime.timedelta(hours=2)
    event.save()
    event.location = "At Alice's place!"
    event.attendees.add(user)
    event.attendees.add(alice)
    event.save()

    event = Event(title="Weekly team meeting", project=tutorial)
    event.start = datetime.datetime.today() + datetime.timedelta(days=4, hours=1)
    event.end = datetime.datetime.today() + datetime.timedelta(days=4, hours=2)
    event.save()
    event.attendees.add(user)
    event.attendees.add(alice)
    event.save()

    event = Event(title="Weekly team meeting", project=tutorial)
    event.start = datetime.datetime.today() - datetime.timedelta(days=3)
    event.end = datetime.datetime.today() - datetime.timedelta(days=3)
    event.save()
    event.attendees.add(user)
    event.attendees.add(alice)
    event.save()


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

    def __str__(self):
        #TODO: remove unnecessary whitespaces
        address = ""

        # if there is at least the street or house_number AND postal_code or city, add a colon (,) between the two parts
        if (self.street != "" or self.house_number) != "" and (self.postal_code != "" or self.city != ""):
            address += self.street + " " + self.house_number + ", " + self.postal_code + " " + self.city
            colon_index = address.index(',')

            # if there's no house_number, there is a space between street and second part and two spaces after the colon, let's remove that
            if address[colon_index-1] == ' ':
                address = address[0:colon_index-1] + address[colon_index:colon_index+1] + address[colon_index+1:]
        # if one of the two separated parts is empty, we don't need a colon
        else:
            address += self.street + " " + self.house_number + " " + self.postal_code + " " + self.city

        return address

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

    def delete_picture(self):
        """
        deletes a picture
        :return:
        """
        self.picture.delete()
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

    def get_name(self):
        if self.first_name is None or self.first_name == "":
            if self.last_name is not None and self.last_name != "":
                return self.last_name
            else:
                return ""
        else:
            if self.last_name is not None and self.last_name != "":
                return self.first_name + " " + self.last_name
            else:
                return self.first_name


    def __str__(self):
        if self.first_name is None and self.last_name is None or self.first_name == '' and self.last_name == '':
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
        create_tutorial_project(user)
        return profile


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=32, unique=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "PasswordResetToken for " + str(self.user.username)
