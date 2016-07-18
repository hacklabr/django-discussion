# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basehistory',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='topic',
            name='categories',
            field=models.ManyToManyField(related_name='topics', verbose_name='categories', to='discussion.Category'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='forum',
            field=models.ForeignKey(related_name='topics', verbose_name='forum', to='discussion.Forum'),
        ),
    ]
