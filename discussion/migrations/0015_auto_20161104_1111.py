# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0014_auto_20160906_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicnotification',
            name='action',
            field=models.CharField(default=b'undefined', max_length=64, choices=[(b'undefined', 'Undefined'), (b'mention', 'Mention'), (b'comment', 'Comment'), (b'new_topic', 'New Topic'), (b'new_comment', 'New Comment'), (b'new_reaction', 'New Reaction'), (b'new_reaction_comment', 'New Reaction to a Comment'), (b'new_activity', 'New activity')]),
        ),
    ]
