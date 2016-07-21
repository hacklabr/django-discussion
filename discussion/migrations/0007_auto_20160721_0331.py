# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0006_commentlike_topiclike_topicuse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basehistory',
            old_name='edited_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='edited_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='edited_at',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(related_name='comments', to='discussion.Topic'),
        ),
    ]
