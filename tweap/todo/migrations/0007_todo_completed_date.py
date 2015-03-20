# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='completed_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
