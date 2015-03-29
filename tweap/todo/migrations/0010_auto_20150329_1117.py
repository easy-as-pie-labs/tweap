# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_auto_20150328_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completed_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
