from django.contrib import admin
from notification_center.models import Notification, Event

admin.site.register(Event)
admin.site.register(Notification)