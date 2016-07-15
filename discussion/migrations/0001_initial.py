# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False, verbose_name='hidden')),
                ('hidden_justification', models.TextField(null=True, verbose_name='Justification', blank=True)),
                ('is_modified', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'comment history',
                'verbose_name_plural': 'comments history',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=124, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, editable=False)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('color', models.CharField(help_text='Title color in hex format (i.e: #1aafd0).', max_length=7, verbose_name='color', blank=True)),
                ('parent', models.ForeignKey(verbose_name='category parent', blank=True, to='discussion.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False, verbose_name='hidden')),
                ('hidden_justification', models.TextField(null=True, verbose_name='Justification', blank=True)),
                ('is_modified', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'text', max_length=64, unique=True, verbose_name='Slug')),
                ('text', models.TextField(verbose_name='comment')),
                ('author', models.ForeignKey(related_name='comment_author', verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('hidden_by', models.ForeignKey(verbose_name='hidden_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(related_name='parent_comment', verbose_name='comment parent', blank=True, to='discussion.Comment', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='text', blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=255, unique=True, verbose_name='Slug')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_private', models.BooleanField(default=False, verbose_name='private')),
                ('author', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(to='discussion.Category', verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False, verbose_name='hidden')),
                ('hidden_justification', models.TextField(null=True, verbose_name='Justification', blank=True)),
                ('is_modified', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=64, unique=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(null=True, verbose_name='content', blank=True)),
                ('is_private', models.BooleanField(default=False, verbose_name='private')),
                ('author', models.ForeignKey(related_name='topic_author', verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='discussion.Category', verbose_name='categories')),
                ('forum', models.ForeignKey(verbose_name='forum', to='discussion.Forum')),
                ('hidden_by', models.ForeignKey(verbose_name='hidden_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('tags', models.ManyToManyField(to='discussion.Tag', verbose_name='tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopicNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(default=b'undefined', max_length=64, choices=[(b'undefined', 'Undefined'), (b'mention', 'Mention'), (b'comment', 'Comment')])),
                ('is_read', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(blank=True, to='discussion.Comment', null=True)),
                ('topic', models.ForeignKey(to='discussion.Topic')),
                ('user', models.ForeignKey(related_name='topic_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-pk'],
                'verbose_name': 'topic notification',
                'verbose_name_plural': 'topics notification',
            },
        ),
        migrations.CreateModel(
            name='CommentHistory',
            fields=[
                ('basehistory_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.BaseHistory')),
                ('text', models.TextField(verbose_name='text')),
            ],
            options={
                'abstract': False,
            },
            bases=('discussion.basehistory',),
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('reaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.Reaction')),
            ],
            bases=('discussion.reaction',),
        ),
        migrations.CreateModel(
            name='TopicHistory',
            fields=[
                ('basehistory_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.BaseHistory')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('topic', models.ForeignKey(verbose_name='original topic', to='discussion.Topic')),
            ],
            options={
                'abstract': False,
            },
            bases=('discussion.basehistory',),
        ),
        migrations.CreateModel(
            name='TopicReaction',
            fields=[
                ('reaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.Reaction')),
            ],
            bases=('discussion.reaction',),
        ),
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(related_name='topics', to='discussion.Topic'),
        ),
        migrations.AddField(
            model_name='basehistory',
            name='author',
            field=models.ForeignKey(related_name='basehistory_author', verbose_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basehistory',
            name='hidden_by',
            field=models.ForeignKey(verbose_name='hidden_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='basehistory',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag', verbose_name='tags'),
        ),
        migrations.CreateModel(
            name='TopicLike',
            fields=[
                ('topicreaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.TopicReaction')),
            ],
            bases=('discussion.topicreaction',),
        ),
        migrations.CreateModel(
            name='TopicUse',
            fields=[
                ('topicreaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='discussion.TopicReaction')),
            ],
            bases=('discussion.topicreaction',),
        ),
        migrations.AddField(
            model_name='topicreaction',
            name='topic',
            field=models.ForeignKey(to='discussion.Topic'),
        ),
        migrations.AlterUniqueTogether(
            name='topicnotification',
            unique_together=set([('user', 'topic')]),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(related_name='likes', to='discussion.Comment'),
        ),
        migrations.AddField(
            model_name='commenthistory',
            name='comment',
            field=models.ForeignKey(verbose_name='original comment', to='discussion.Comment'),
        ),
    ]
