# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_management', '0004_project_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000, blank=True, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('attendees', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(to='project_management.Project')),
                ('tags', models.ManyToManyField(blank=True, to='project_management.Tag', null=True)),
            ],
            options={
                'ordering': ['start', 'project__name'],
            },
            bases=(models.Model,),
        ),
    ]
