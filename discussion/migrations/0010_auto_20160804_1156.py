# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0009_commentfile_topicfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfile',
            name='comment',
            field=models.ForeignKey(related_name='attachment', to='discussion.Comment'),
        ),
        migrations.AlterField(
            model_name='topicfile',
            name='topic',
            field=models.ForeignKey(related_name='attachment', to='discussion.Topic'),
        ),
    ]
