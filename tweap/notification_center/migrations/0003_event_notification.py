# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification_center', '0002_auto_20150206_0057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='notification_center.Event')),
                ('project', models.ForeignKey(to='project_management.Project')),
                ('receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notification_receiver')),
                ('trigger', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notification_triggerer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
