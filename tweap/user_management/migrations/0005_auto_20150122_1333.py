# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_auto_20150122_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address_id',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='profileaddress',
            old_name='PostalCode_id',
            new_name='PostalCode',
        ),
    ]
