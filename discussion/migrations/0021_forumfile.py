# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import discussion.models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0020_auto_20171211_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('file', models.FileField(upload_to=discussion.models.get_upload_path)),
                ('forum', models.ForeignKey(related_name='files', on_delete=models.CASCADE, blank=True, to='discussion.Forum', null=True)),
            ],
        ),
    ]
