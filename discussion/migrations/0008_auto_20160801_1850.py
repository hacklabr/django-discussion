# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_auto_20160729_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='categories',
            field=models.ManyToManyField(related_name='topics', verbose_name='categories', to='discussion.Category', blank=True),
        ),
    ]
