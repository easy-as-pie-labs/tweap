# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='icon',
            field=models.CharField(default='fa fa-folder-open-o', max_length=30),
            preserve_default=True,
        ),
    ]
