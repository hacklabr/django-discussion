# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0006_auto_20160728_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicnotification',
            name='comment_like',
            field=models.ForeignKey(blank=True, on_delete=models.CASCADE, to='discussion.CommentLike', null=True),
        ),
        migrations.AddField(
            model_name='topicnotification',
            name='topic_like',
            field=models.ForeignKey(blank=True, on_delete=models.CASCADE, to='discussion.TopicLike', null=True),
        ),
    ]
