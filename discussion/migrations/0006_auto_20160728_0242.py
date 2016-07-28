# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_auto_20160726_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basehistory',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag', verbose_name='tags', blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag', verbose_name='tags', blank=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.ManyToManyField(to='discussion.Category', verbose_name='category', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag', verbose_name='tags', blank=True),
        ),
    ]
