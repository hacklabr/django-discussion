from actstream import action

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template import Template, Context
from django.core.mail import EmailMessage

from discussion.models import Comment, CommentHistory, TopicNotification, TopicLike, TopicUse, CommentLike
from courses_notifications.models import unread_notification_increment
from courses.models import EmailTemplate

import re


def get_email_info(lang, notif_type):
    email_info = {'subject': '', 'content': ''}

    if notif_type == 'comment':
        if lang == 'es':
            email_info = {'subject': 'Nuevo Comentario', 'content': '{} comentó sobre el tema {} en el foro {}'}
        elif lang == 'pt_br':
            email_info = {'subject': 'New Comment', 'content': '{} comentou no tópico {} no fórum {}'}
        elif lang == 'en':
            email_info = {'subject': 'Novo Comentário', 'content': '{} commented on topic {} in forum {}'}
    elif notif_type == 'comment_reaction':
        if lang == 'es':
            email_info = {'subject': 'Reacción al comentario', 'content': 'A {} le gustó un comentario en el tema {} del foro {}'}
        elif lang == 'pt_br':
            email_info = {'subject': 'Comment Reaction', 'content': '{} gostou de um comentário no tópico {} no fórum {}'}
        elif lang == 'en':
            email_info = {'subject': 'Reação ao comentário', 'content': '{} liked a comment at topic {} in forum {}'}
    elif notif_type == 'topic_reaction':
        if lang == 'es':
            email_info = {'subject': 'Reacción al tema', 'content': 'A {} le gustó el tema {} en el foro {}.'}
        elif lang == 'pt_br':
            email_info = {'subject': 'Topic Reaction', 'content': '{} gostou do tópico {} no fórum {}.'}
        elif lang == 'en':
            email_info = {'subject': 'Reação aoa tópico', 'content': '{} liked the topic {} in forum {}.'}

    return email_info


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def send(bcc, message, subject, email_batch_size):
    # Iterate over the bcc list to send emails in chunks
    # Maximum chunk size is email_batch_size
    start = 0
    end = min(email_batch_size, len(bcc))
    while start < len(bcc):
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,
                             [settings.DEFAULT_FROM_EMAIL, ], bcc[start:end])
        email.content_subtype = 'html'
        email.send()
        start = end
        end = min(end + email_batch_size, len(bcc))

def send_emails(users, notif_type, notif_author, topic, forum, instance):
    try:
        et = EmailTemplate.objects.get(name='notification')
    except EmailTemplate.DoesNotExist:
        et = EmailTemplate(name='notification', subject='{{subject}}', template='{{message|safe}}')

    email_batch_size = settings.PROFESSOR_MESSAGE_CHUNK_SIZE
    origin = 'https://' + settings.SITE_DOMAIN

    if settings.I18N_SUPPORT:
        bcc_es = [u.email for u in users if u.is_active and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", u.email) and u.preferred_language == 'es']
        bcc_pt_br = [u.email for u in users if u.is_active and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", u.email) and u.preferred_language == 'pt-br']
        bcc_en = [u.email for u in users if u.is_active and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", u.email) and u.preferred_language == 'en']

        comment_text = ''
        if notif_type == "comment" or notif_type == "comment_reaction":
            text = instance.text if notif_type == 'comment' else instance.comment.text
            comment_text = ':\n\n"{}"\n'.format(cleanhtml(text))

        email_info_es = get_email_info('es', notif_type)
        subject_es = email_info_es['subject']
        message_es = email_info_es['content'].format(notif_author, topic.title, forum.title)
        message_es += comment_text
        message_es += '\nPuede acceder al tema mencionado en {}/#!/topic/{}'.format(origin, topic.id)
        subject_es = Template(et.subject).render(Context({'subject': subject_es}))
        message_es = Template(et.template).render(Context({'message': message_es}))
        send(bcc_es, message_es, subject_es, email_batch_size)

        email_info_pt_br = get_email_info('pt_br', notif_type)
        subject_pt_br = email_info_pt_br['subject']
        message_pt_br = email_info_pt_br['content'].format(notif_author, topic.title, forum.title)
        message_pt_br += comment_text
        message_pt_br += '\nVocê pode acessar o tópico mencionado em {}/#!/topic/{}'.format(origin, topic.id)
        subject_pt_br = Template(et.subject).render(Context({'subject': subject_pt_br}))
        message_pt_br = Template(et.template).render(Context({'message': message_pt_br}))
        send(bcc_pt_br, message_pt_br, subject_pt_br, email_batch_size)

        email_info_en = get_email_info('en', notif_type)
        subject_en = email_info_en['subject']
        message_en = email_info_en['content'].format(notif_author, topic.title, forum.title)
        message_en += comment_text
        message_en += '\nYou can acess the mentioned topic at {}/#!/topic/{}'.format(origin, topic.id)
        subject_en = Template(et.subject).render(Context({'subject': subject_en}))
        message_en = Template(et.template).render(Context({'message': message_en}))
        send(bcc_en, message_en, subject_en, email_batch_size)


@receiver(post_save, sender=Comment)
def comment_created_or_updated(instance, **kwargs):
    action.send(instance.author, verb='created comment', action_object=instance.topic, target=instance.topic.forum)

    # if instance.topic.forum.forum_type == 'activity':
    #    return
    # if this comment was just updated, no notifications must be sent
    if kwargs['created'] is False:
        return

    # Adjust last_activity_at in Topic
    instance.topic.last_activity_at = instance.updated_at
    instance.topic.save()

    # Users that must be notified
    users = []

    # Trigger: a comment has been made
    # Trigger: an answer to a comment has been made
    # Notify the topic creator
    users.append(instance.topic.author)

    # Trigger: a comment has been made
    # Trigger: an answer to a comment has been made
    # Notify anyone who has reacted to the main topic message
    for react in TopicLike.objects.filter(topic=instance.topic):
        users.append(react.user)

    for react in TopicUse.objects.filter(topic=instance.topic):
        users.append(react.user)

    if not instance.parent:  # If the comment is not an answer to another comment
        # Trigger: a comment has been made
        # Notify people that already commented ou answered to comments in this topic
        for comment in Comment.objects.filter(topic=instance.topic):
            users.append(comment.author)
    else:
        # Trigger: an answer to a comment has been made
        # Notify the author of the parent comment
        users.append(instance.parent.author)

        for react in CommentLike.objects.filter(comment=instance.parent):
            # Trigger: an answer to a comment has been made
            # Notify people that have reacted to the parent comment
            users.append(react.user)

        for comment in Comment.objects.filter(topic=instance.topic, parent=instance.parent):
            # Trigger: an answer to a comment has been made
            # Notify who has answered the same parent comment
            users.append(comment.author)

            for react in CommentLike.objects.filter(comment=comment):
                # Trigger: an answer to a comment has been made
                # Notify people that have reacted to answers to the parent comment
                users.append(react.user)

    # Remove the original author from the notifications list
    users = list(set([user for user in users if user != instance.author]))

    # Create (or update) the nedded notifications
    for one_user in users:
        # Check if the current user already has a pending notification for this topic
        try:
            notification = TopicNotification.objects.get(
                user=one_user,
                topic=instance.topic,
            )
        except TopicNotification.DoesNotExist:
            notification = TopicNotification.objects.create(
                user=one_user,
                topic=instance.topic,
                comment=instance,
            )

        notification.action = 'new_comment'
        notification.comment = instance
        notification.is_read = False
        notification.save()

        # Increase the unread count for this user in 1
        unread_notification_increment(one_user)


    notif_author = instance.author.first_name or instance.author.username
    topic = instance.topic
    forum = instance.topic.forum
    send_emails(users, "comment", notif_author, topic, forum, instance)

    coment_revision = CommentHistory()
    coment_revision.create_or_update_revision(instance=instance)


@receiver(post_save, sender=TopicLike)
@receiver(post_save, sender=TopicUse)
def topic_reaction_created_or_updated(instance, **kwargs):
    action.send(instance.user, verb='reacted', action_object=instance.topic, target=instance.topic.forum)

    # if instance.topic.forum.forum_type == 'activity':
    #    return

    # Users that must be notified
    users = []

    # Trigger: reaction to a topic
    # Notify topic creator
    users.append(instance.topic.author)

    # Trigger: reaction to a topic
    # Notify everybody that has reacted to the topic
    for react in TopicLike.objects.filter(topic=instance.topic):
        users.append(react.user)

    for react in TopicUse.objects.filter(topic=instance.topic):
        users.append(react.user)

    # Remove the original reaction author from the notifications list
    users = list(set([user for user in users if user != instance.user]))

    # Create (or update) the nedded notifications
    for one_user in users:
        # Check if the current user already has a pending notification for this topic
        try:
            notification = TopicNotification.objects.get(
                user=one_user,
                topic=instance.topic,
            )
        except TopicNotification.DoesNotExist:
            notification = TopicNotification.objects.create(
                user=one_user,
                topic=instance.topic,
            )

        notification.action = 'new_reaction'
        notification.is_read = False
        notification.topic_like = instance
        notification.save()

        # Increase the unread count for this user in 1
        unread_notification_increment(one_user)

    notif_author = instance.user.first_name or instance.user.username
    topic = instance.topic
    forum = instance.topic.forum
    send_emails(users, "topic_reaction", notif_author, topic, forum, instance)

@receiver(post_save, sender=CommentLike)
def comment_reaction_created_or_updated(instance, **kwargs):
    action.send(instance.user, verb='reacted', action_object=instance.comment.topic, target=instance.comment.topic.forum)

    # if instance.comment.topic.forum.forum_type != 'activity':
    #    return
    # Users that must be notified
    users = []

    # Trigger: reaction to a comment
    # Trigger: reaction to an answer of a comment
    # Notify topic creator
    users.append(instance.comment.topic.author)

    # Trigger: reaction to a comment
    # Trigger: reaction to an answer of a comment
    # Notify the comment/answer author
    users.append(instance.comment.author)

    if not instance.comment.parent:  # If this comment is not an answer
        # Trigger: reaction to a comment
        # Notify who has already reacted to the comment
        for react in CommentLike.objects.filter(comment=instance.comment):
            users.append(react.user)
    else:  # If this comment is an answer to another comment
        # Trigger: reaction to an answer of a comment
        # Notify the author of the parent comment
        users.append(instance.comment.parent.author)

        # Trigger: reaction to an answer of a comment
        # Notify who has already answered the same parent comment
        for answer in Comment.objects.filter(parent=instance.comment.parent):
            users.append(answer.author)

        # Trigger: reaction to an answer of a comment
        # Notify who has reacted to the parent comment
        for react in CommentLike.objects.filter(comment=instance.comment.parent):
            users.append(react.user)

    # Remove the original author from the notifications list
    users = list(set([user for user in users if user != instance.user]))

    # Create (or update) the nedded notifications
    for one_user in users:
        # Check if the current user already has a pending notification for this comment
        try:
            notification = TopicNotification.objects.get(
                user=one_user,
                topic=instance.comment.topic,
            )
        except TopicNotification.DoesNotExist:
            notification = TopicNotification.objects.create(
                user=one_user,
                topic=instance.comment.topic,
            )

        notification.comment = instance.comment
        notification.action = 'new_reaction_comment'
        notification.is_read = False
        notification.comment_like = instance
        notification.save()

        # Increase the unread count for this user in 1
        unread_notification_increment(one_user)

    notif_author = instance.user.first_name or instance.user.username
    topic = instance.comment.topic
    forum = instance.comment.topic.forum
    send_emails(users, "comment_reaction", notif_author, topic, forum, instance)

def topic_viewed(request, topic):
    # Todo test detail views
    user = request.user
    comment_number = CommentBookmark.page_to_comment_number(request.GET.get('page', 1))

    CommentBookmark.update_or_create(
        user=user,
        topic=topic,
        comment_number=comment_number
    )
    TopicNotification.mark_as_read(user=user, topic=topic)
    TopicUnread.create_or_mark_as_read(user=user, topic=topic)
    topic.increase_view_count()
