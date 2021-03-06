from actstream import action
from django.db.models.signals import post_save
from django.dispatch import receiver
from discussion.models import Comment, CommentHistory, TopicNotification, TopicLike, TopicUse, CommentLike
from courses_notifications.models import unread_notification_increment


@receiver(post_save, sender=Comment)
def comment_created_or_updated(instance, **kwargs):
    action.send(instance.author, verb='created comment', action_object=instance.topic, target=instance.topic.forum)

    if instance.topic.forum.forum_type != 'discussion':
        return
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
    users = [user for user in users if user != instance.author]

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

    coment_revision = CommentHistory()
    coment_revision.create_or_update_revision(instance=instance)


@receiver(post_save, sender=TopicLike)
@receiver(post_save, sender=TopicUse)
def topic_reaction_created_or_updated(instance, **kwargs):
    action.send(instance.user, verb='reacted', action_object=instance.topic, target=instance.topic.forum)

    if instance.topic.forum.forum_type != 'discussion':
        return

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
    users = [user for user in users if user != instance.user]

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

@receiver(post_save, sender=CommentLike)
def comment_reaction_created_or_updated(instance, **kwargs):
    action.send(instance.user, verb='reacted', action_object=instance.comment.topic, target=instance.comment.topic.forum)

    if instance.comment.topic.forum.forum_type != 'discussion':
        return
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
    users = [user for user in users if user != instance.user]

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
        # unread_notification_increment(one_user)

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
