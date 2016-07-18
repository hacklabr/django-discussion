# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0003_auto_20160718_0016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
    ]
