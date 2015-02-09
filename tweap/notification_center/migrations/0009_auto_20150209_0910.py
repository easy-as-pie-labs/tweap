# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0008_auto_20150206_0130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='trigger',
            new_name='trigger_user',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='url',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
        migrations.AddField(
            model_name='notification',
            name='target_url',
            field=models.CharField(max_length=100, default='www.google.de'),
            preserve_default=False,
        ),
    ]
