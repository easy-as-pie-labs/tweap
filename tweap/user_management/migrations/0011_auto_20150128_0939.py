# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0010_auto_20150127_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddress',
            name='city',
            field=models.CharField(null=True, max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profileaddress',
            name='house_number',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profileaddress',
            name='postal_code',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='PostalCode',
        ),
        migrations.AlterField(
            model_name='profileaddress',
            name='street',
            field=models.CharField(null=True, max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
