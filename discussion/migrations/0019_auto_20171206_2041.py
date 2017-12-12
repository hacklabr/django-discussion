# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0018_contentfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='groups',
            field=models.ManyToManyField(help_text='The Groups that can have access to this forum. If empty, there are no group restrictions.', related_name='foruns', verbose_name='groups', to='auth.Group', blank=True),
        ),
    ]
