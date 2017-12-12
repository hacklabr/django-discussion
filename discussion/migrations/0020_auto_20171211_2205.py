# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0019_auto_20171206_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='forum_type',
            field=models.CharField(default=b'discussion', max_length=64, verbose_name='Forum Type', choices=[(b'discussion', 'Discussion'), (b'activity', 'Activity')]),
        ),
        migrations.AlterField(
            model_name='forum',
            name='groups',
            field=models.ManyToManyField(help_text='The Groups that can access this forum. If empty, there are no group restrictions.', related_name='foruns', verbose_name='groups', to='auth.Group', blank=True),
        ),
    ]
