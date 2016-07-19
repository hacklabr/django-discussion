# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_("category parent"), null=True, blank=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))

    name = models.CharField(_("title"), max_length=124)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(_("description"), blank=True)
    color = models.CharField(_("color"), max_length=7, blank=True,
                             help_text=_("Title color in hex format (i.e: #1aafd0)."))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Forum(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    category = models.ManyToManyField(Category, verbose_name=_('category'))

    title = models.CharField(_('Title'), max_length=255)
    text = models.TextField(_('text'), blank=True)
    slug = AutoSlugField(_('Slug'), populate_from='title', max_length=255, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    is_private = models.BooleanField(_("private"), default=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name


class BasePost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), related_name=_('%(class)s_author'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'))

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    edited_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(verbose_name=_('hidden'), default=False)
    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('hidden_by'),
        null=True, blank=True)
    # FIXME hidden_notice?
    hidden_justification = models.TextField(_('Justification'), null=True, blank=True)

    is_modified = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def likes_count(self):
        pass

    @property
    def uses_count(self):
        pass


class Topic(BasePost):

    forum = models.ForeignKey(Forum, verbose_name=_('forum'), related_name='topics')
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='topics')

    slug = AutoSlugField(_('Slug'), populate_from='title', max_length=64, editable=False, unique=True)
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('content'), null=True, blank=True)

    is_private = models.BooleanField(_("private"), default=False)

    def __str__(self):
        return self.title

    # @property
    # def count_votes(self):
    #     return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0


class Comment(BasePost):
    parent = models.ForeignKey('self', verbose_name=_("comment parent"), related_name='parent_comment', null=True, blank=True)
    topic = models.ForeignKey(Topic, related_name='topics')

    slug = AutoSlugField(_('Slug'), populate_from='text', max_length=64, editable=False, unique=True)
    text = models.TextField(_('comment'))

    # @property
    # def count_votes(self):
    #     return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0

    def __str__(self):
        return self.title + ' | ' + self.text


class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    timestamp = models.DateTimeField(auto_now=True)


class TopicReaction(Reaction):
    topic = models.ForeignKey(Topic)


class TopicUse(TopicReaction):
    pass


class TopicLike(TopicReaction):
    pass


class CommentLike(Reaction):
    comment = models.ForeignKey(Comment, related_name='likes')


class TopicNotification(models.Model):
    ACTION_CHOICES = (
        ('undefined', _("Undefined")),
        ('mention', _("Mention")),
        ('comment', _("Comment")),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topic_notifications')
    topic = models.ForeignKey('Topic')
    comment = models.ForeignKey('Comment', null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(choices=ACTION_CHOICES, default='undefined', max_length=64)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-date', '-pk']
        verbose_name = _("topic notification")
        verbose_name_plural = _("topics notification")

    def get_absolute_url(self):
        return self.comment.get_absolute_url()

    @property
    def text_action(self):
        return ACTION_CHOICES[self.action][1]

    @property
    def is_mention(self):
        return self.action == 'mention'

    @property
    def is_comment(self):
        return self.action == 'comment'

    @classmethod
    def mark_as_read(cls, user, topic):
        if not user.is_authenticated():
            return

        cls.objects\
            .filter(user=user, topic=topic)\
            .update(is_read=True)


class BaseHistory(BasePost):

    class Meta:
        # ordering = ['-last_edit', '-pk']
        verbose_name = _("comment history")
        verbose_name_plural = _("comments history")

    def create_or_update_revision(self, instance):
        self.author = instance.author
        # if instance.tags:
        #     self.tags = instance.tags
        self.last_edit = instance.timestamp
        self.is_hidden = instance.is_hidden
        self.hidden_by = instance.hidden_by
        self.hidden_justification = instance.hidden_justification
        self.is_modified = instance.is_modified
        self.ip_address = instance.ip_address

        self.save()


class TopicHistory(BaseHistory):
    topic = models.ForeignKey('topic', verbose_name=_("original topic"))
    title = models.CharField(_('title'), max_length=255)
    text = models.TextField(_('text'))


class CommentHistory(BaseHistory):
    comment = models.ForeignKey('Comment', verbose_name=_("original comment"))
    text = models.TextField(_('text'))

    def create_or_update_revision(self, instance):
        self.comment = instance
        self.text = instance.text
        super(CommentHistory, self).create_or_update_revision(instance)
