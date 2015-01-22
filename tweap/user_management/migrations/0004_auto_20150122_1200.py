# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_management', '0003_auto_20150122_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_id',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='address_id',
            field=models.ForeignKey(null=True, blank=True, to='user_management.ProfileAddress'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
