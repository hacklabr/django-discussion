# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='last_activity_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 22, 23, 4, 42, 220698, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topicnotification',
            name='action',
            field=models.CharField(default=b'undefined', max_length=64, choices=[(b'undefined', 'Undefined'), (b'mention', 'Mention'), (b'comment', 'Comment'), (b'new_topic', 'New Topic'), (b'new_comment', 'New Comment')]),
        ),
        migrations.AlterField(
            model_name='topicnotification',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
