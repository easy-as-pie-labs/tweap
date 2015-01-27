# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_auto_20150123_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, upload_to=user_management.models.get_filename, null=True),
            preserve_default=True,
        ),
    ]
