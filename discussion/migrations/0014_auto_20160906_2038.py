# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0013_forum_forum_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='last_activity_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
