from django.contrib import admin
from notification_center.models import Notification, Event, Url

admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(Url)