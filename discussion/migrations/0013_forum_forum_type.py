# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0012_auto_20160814_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='forum_type',
            field=models.CharField(default=b'discussion', max_length=64, choices=[(b'discussion', 'Discussion'), (b'activity', 'Activity')]),
        ),
    ]
