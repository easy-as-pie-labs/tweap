# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0005_auto_20150206_0112'),
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
        migrations.RemoveField(
            model_name='notification',
            name='url',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.RemoveField(
            model_name='urlparameter',
            name='url',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
        migrations.DeleteModel(
            name='UrlParameter',
        ),
    ]
