# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0004_auto_20160718_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentlike',
            name='reaction_ptr',
        ),
        migrations.RemoveField(
            model_name='reaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='topiclike',
            name='topicreaction_ptr',
        ),
        migrations.RemoveField(
            model_name='topicreaction',
            name='reaction_ptr',
        ),
        migrations.RemoveField(
            model_name='topicreaction',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='topicuse',
            name='topicreaction_ptr',
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
        migrations.DeleteModel(
            name='CommentLike',
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
        migrations.DeleteModel(
            name='TopicLike',
        ),
        migrations.DeleteModel(
            name='TopicReaction',
        ),
        migrations.DeleteModel(
            name='TopicUse',
        ),
    ]
