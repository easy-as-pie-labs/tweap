# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_auto_20150122_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profileaddress',
            old_name='postalCode',
            new_name='postal_code',
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(blank=True, null=True, max_length=50),
            preserve_default=True,
        ),
    ]
