# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0007_auto_20150206_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlparameter',
            name='url',
        ),
        migrations.DeleteModel(
            name='UrlParameter',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='text',
            new_name='url',
        ),
        migrations.AddField(
            model_name='url',
            name='parameter',
            field=models.CharField(default=20, max_length=20),
            preserve_default=False,
        ),
    ]
