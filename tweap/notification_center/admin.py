from django.contrib import admin
from notification_center.models import Notification, NotificationEvent

admin.site.register(NotificationEvent)
admin.site.register(Notification)