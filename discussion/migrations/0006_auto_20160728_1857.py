# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_auto_20160726_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicnotification',
            name='comment_like',
            field=models.ForeignKey(blank=True, to='discussion.CommentLike', null=True),
        ),
        migrations.AddField(
            model_name='topicnotification',
            name='topic_like',
            field=models.ForeignKey(blank=True, to='discussion.TopicLike', null=True),
        ),
    ]
