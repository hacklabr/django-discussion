# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0015_auto_20161104_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicnotification',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
