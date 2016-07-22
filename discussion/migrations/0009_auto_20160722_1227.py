# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_auto_20160722_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='is_private',
        ),
        migrations.AddField(
            model_name='forum',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='public'),
        ),
    ]
