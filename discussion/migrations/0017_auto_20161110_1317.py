# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0016_auto_20161107_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_read', models.BooleanField(default=False)),
                ('topic', models.ForeignKey(related_name='read', to='discussion.Topic')),
                ('user', models.ForeignKey(related_name='topicread', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='topicread',
            unique_together=set([('user', 'topic')]),
        ),
    ]
