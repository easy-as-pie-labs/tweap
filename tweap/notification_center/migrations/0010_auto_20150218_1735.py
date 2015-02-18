# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0009_auto_20150209_0910'),
    ]

    operations = [
        migrations.RenameModel('Event', 'NotificationEvent'),
    ]
