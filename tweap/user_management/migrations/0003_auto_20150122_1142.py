# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20150122_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address_id',
            field=models.ForeignKey(null=True, to='user_management.ProfileAddress'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.CharField(null=True, max_length=50),
            preserve_default=True,
        ),
    ]
