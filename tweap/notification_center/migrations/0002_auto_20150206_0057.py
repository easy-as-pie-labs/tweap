# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='project',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='trigger',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
