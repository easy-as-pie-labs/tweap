# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(null=True, blank=True, max_length=1000)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='project_management.Project')),
                ('tags', models.ManyToManyField(to='project_management.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
