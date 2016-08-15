# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0011_auto_20160811_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfile',
            name='comment',
            field=models.ForeignKey(related_name='files', blank=True, to='discussion.Comment', null=True),
        ),
        migrations.AlterField(
            model_name='topicfile',
            name='topic',
            field=models.ForeignKey(related_name='files', blank=True, to='discussion.Topic', null=True),
        ),
    ]
