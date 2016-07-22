# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_auto_20160721_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='is_private',
        ),
        migrations.AddField(
            model_name='topic',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='public'),
        ),
        migrations.AlterField(
            model_name='forum',
            name='author',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='topicnotification',
            name='action',
            field=models.CharField(default=b'undefined', max_length=64, choices=[(b'undefined', 'Undefined'), (b'mention', 'Mention'), (b'comment', 'Comment'), (b'new_topic', 'New Topic')]),
        ),
    ]
