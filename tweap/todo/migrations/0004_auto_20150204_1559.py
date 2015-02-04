# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_todo_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='completed',
            new_name='done',
        ),
    ]
