# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_auto_20150122_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profileaddress',
            old_name='PostalCode',
            new_name='postalCode',
        ),
    ]
