# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0002_auto_20160718_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='basehistory',
            name='edited_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 3, 15, 58, 107641, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='edited_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 3, 16, 22, 862642, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='edited_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 3, 16, 26, 319461, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
