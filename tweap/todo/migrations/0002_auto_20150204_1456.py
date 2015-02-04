# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='assignees',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='todo',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='project_management.Tag'),
            preserve_default=True,
        ),
    ]
