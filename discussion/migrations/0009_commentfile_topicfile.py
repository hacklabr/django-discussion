# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import discussion.models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_auto_20160801_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('file', models.FileField(upload_to=discussion.models.get_upload_path)),
                ('comment', models.ForeignKey(related_name='comment', on_delete=models.CASCADE, to='discussion.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='TopicFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('file', models.FileField(upload_to=discussion.models.get_upload_path)),
                ('topic', models.ForeignKey(related_name='topic', on_delete=models.CASCADE, to='discussion.Topic')),
            ],
        ),
    ]
