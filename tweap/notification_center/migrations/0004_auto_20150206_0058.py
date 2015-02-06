# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0003_event_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
