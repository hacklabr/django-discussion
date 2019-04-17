# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0010_auto_20160804_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfile',
            name='comment',
            field=models.ForeignKey(related_name='files', on_delete=models.CASCADE, to='discussion.Comment'),
        ),
        migrations.AlterField(
            model_name='topicfile',
            name='topic',
            field=models.ForeignKey(related_name='files', on_delete=models.CASCADE, to='discussion.Topic'),
        ),
    ]
