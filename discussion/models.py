from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone
import hashlib


class Category(models.Model):
    parent = models.ForeignKey('self', models.CASCADE, verbose_name=_("category parent"), null=True, blank=True)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))

    name = models.CharField(_("title"), max_length=124)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(_("description"), blank=True)
    color = models.CharField(_("color"), max_length=7, blank=True,
                             help_text=_("Title color in hex format (i.e: #1aafd0)."))

    def __str__(self):
        return self.name


class Forum(models.Model):

    TYPE_CHOICES = (
        ('discussion', _('Discussion')),
        ('activity', _('Activity')),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('User'), blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name=_('category'), blank=True)

    title = models.CharField(_('Title'), max_length=255)
    text = models.TextField(_('text'), blank=True)
    slug = AutoSlugField(_('Slug'), populate_from='title', max_length=255, editable=False, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    forum_type = models.CharField(_('Forum Type'), choices=TYPE_CHOICES, default='discussion', max_length=64)

    is_public = models.BooleanField(_("public"), default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The Groups that can access this forum. If empty, there are no group restrictions.'),
        related_name="foruns",
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    instance.file.open()
    content = instance.file.read()
    hash_name = hashlib.sha1(content).hexdigest()
    if isinstance(instance, TopicFile) and hasattr(instance, 'topic') and instance.topic:
        return u'forum/{}/{}_{}'.format(instance.topic.slug, hash_name, instance.name)
    elif isinstance(instance, CommentFile) and hasattr(instance, 'topic') and instance.topic:
        return u'forum/{}/{}/{}_{}'.format(instance.comment.topic.slug, instance.comment.slug, hash_name, instance.name)
    elif isinstance(instance, ContentFile):
        return u'forum/content/{}_{}'.format(hash_name, instance.name)
    else:
        return u'forum/{}_{}'.format(hash_name, instance.name)


class ForumFile(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    forum = models.ForeignKey('Forum', related_name='files', null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path)

    def __unicode__(self):
        return self.name


class TopicFile(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    topic = models.ForeignKey('Topic', models.CASCADE, related_name='files', null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path)

    def __unicode__(self):
        return self.name


class CommentFile(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    comment = models.ForeignKey('Comment', models.CASCADE, related_name='files', null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path)

    def __unicode__(self):
        return self.name


class ContentFile(models.Model):
    name = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=get_upload_path)

    def __unicode__(self):
        return self.name


class BasePost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('author'), related_name=_('%(class)s_author'))
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_hidden = models.BooleanField(verbose_name=_('hidden'), default=False)
    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('hidden_by'),
        null=True, blank=True)
    # FIXME hidden_notice?
    hidden_justification = models.TextField(_('Justification'), null=True, blank=True)

    is_modified = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        abstract = True


class Topic(BasePost):

    forum = models.ForeignKey(Forum, models.CASCADE, verbose_name=_('forum'), related_name='topics')
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name='topics', blank=True)

    last_activity_at = models.DateTimeField(auto_now=True)

    slug = AutoSlugField(_('Slug'), populate_from='title', max_length=64, editable=False, unique=True)
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('content'), null=True, blank=True)

    is_public = models.BooleanField(_("public"), default=False)

    def __str__(self):
        return self.title

    @property
    def count_likes(self):
        return self.likes.count()

    @property
    def count_uses(self):
        return self.uses.count()

    @property
    def count_replies(self):
        return self.comments.count()


class TopicRead(models.Model):
    topic = models.ForeignKey(Topic, models.CASCADE, related_name='read')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('user'), related_name=_('%(class)s'))
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.topic.title + " " + self.user.username + " " + str(self.is_read)

    class Meta:
        unique_together = ('user', 'topic')


class Comment(BasePost):
    parent = models.ForeignKey('self',
                               models.CASCADE,
                               verbose_name=_("comment parent"),
                               related_name='comment_replies',
                               null=True, blank=True)
    topic = models.ForeignKey(Topic, models.CASCADE, related_name='comments')

    slug = AutoSlugField(_('Slug'), populate_from='text', max_length=64, editable=False, unique=True)
    text = models.TextField(_('text'))

    @property
    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.text


class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('User'))
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TopicUse(Reaction):
    topic = models.ForeignKey(Topic, models.CASCADE, related_name='uses')

    class Meta:
        unique_together = ('user', 'topic')


class TopicLike(Reaction):
    topic = models.ForeignKey(Topic, models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'topic')


class CommentLike(Reaction):
    comment = models.ForeignKey(Comment, models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'comment')


class TopicNotification(models.Model):
    ACTION_CHOICES = (
        ('undefined', _("Undefined")),
        ('mention', _("Mention")),
        ('comment', _("Comment")),
        ('new_topic', _("New Topic")),
        ('new_comment', _("New Comment")),
        ('new_reaction', _("New Reaction")),
        ('new_reaction_comment', _("New Reaction to a Comment")),
        ('new_activity', _("New activity")),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='topic_notifications')
    topic = models.ForeignKey('Topic', models.CASCADE,)
    comment = models.ForeignKey('Comment', models.CASCADE, null=True, blank=True)
    comment_like = models.ForeignKey('CommentLike', models.CASCADE, null=True, blank=True)
    topic_like = models.ForeignKey('TopicLike', models.CASCADE, null=True, blank=True)

    date = models.DateTimeField()
    action = models.CharField(choices=ACTION_CHOICES, default='undefined', max_length=64)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-date', '-pk']
        verbose_name = _("topic notification")
        verbose_name_plural = _("topics notification")

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_date', False):
            self.date = timezone.now()

        super(TopicNotification, self).save(*args, **kwargs)

    @property
    def text_action(self):
        return self.ACTION_CHOICES[self.action][1]

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
        self.last_edit = instance.updated_at
        self.is_hidden = instance.is_hidden
        self.hidden_by = instance.hidden_by
        self.hidden_justification = instance.hidden_justification
        self.is_modified = instance.is_modified
        self.ip_address = instance.ip_address

        self.save()


class TopicHistory(BaseHistory):
    topic = models.ForeignKey('topic', models.CASCADE, verbose_name=_("original topic"))
    title = models.CharField(_('title'), max_length=255)
    text = models.TextField(_('text'))


class CommentHistory(BaseHistory):
    comment = models.ForeignKey('Comment', models.CASCADE, verbose_name=_("original comment"))
    text = models.TextField(_('text'))

    def create_or_update_revision(self, instance):
        self.comment = instance
        self.text = instance.text
        super(CommentHistory, self).create_or_update_revision(instance)
