from django.db.models.signals import post_save
from django.dispatch import receiver
from discussion.models import Topic, Comment, CommentHistory, TopicNotification, TopicLike, TopicUse, CommentLike
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Topic)
def topic_created_or_updated(instance, **kwargs):

    # Adjust last_activity_at in Topic
    instance.last_activity_at = instance.updated_at

    User = get_user_model()
    forum = instance.forum

    # Users that must be notified
    users = []

    # If the topic is an answer, usual notification rules don't apply
    # The detection can be made by using the forum number as reference
    # If its greater then 13, the forum must be a activity specific one
    if instance.forum.id > 13:
        # This topic is an answer to a discussion activity
        # Whoever has access to the same course must be notified
        pass

    else:
        # This is a regular topic
        if forum.is_public is True:  # if the forum is public, every user should be notified and the groups check is not necessary
            users = User.objects.all()
        else:  # if the forum is not public, only members from groups registered in the forum must be notified
            for group in forum.groups.all():
                for u in User.objects.filter(groups=group):
                    users.append(u)

    # Remove the original author from the notifications list
    users = [user for user in users if user != instance.author]

    for one_user in users:
        try:
            notification = TopicNotification.objects.get(
                user=one_user,
                topic=instance,
            )
        except TopicNotification.DoesNotExist:
            notification = TopicNotification.objects.create(
                user=one_user,
                topic=instance,
                action='new_topic',
            )

        # Create the New Topic notification for appropriate users
        notification.is_read = False
        notification.save()


@receiver(post_save, sender=Comment)
def comment_created_or_updated(instance, **kwargs):

    # Adjust last_activity_at in Topic
    instance.topic.last_activity_at = instance.updated_at

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

    coment_revision = CommentHistory()
    coment_revision.create_or_update_revision(instance=instance)


@receiver(post_save, sender=TopicLike)
@receiver(post_save, sender=TopicUse)
def topic_reaction_created_or_updated(instance, **kwargs):

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


@receiver(post_save, sender=CommentLike)
def comment_reaction_created_or_updated(instance, **kwargs):

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


# def topic_viewed(request, topic):
#     # Todo test detail views
#     user = request.user
#     comment_number = CommentBookmark.page_to_comment_number(request.GET.get('page', 1))
#
#     CommentBookmark.update_or_create(
#         user=user,
#         topic=topic,
#         comment_number=comment_number
#     )
#     TopicNotification.mark_as_read(user=user, topic=topic)
#     TopicUnread.create_or_mark_as_read(user=user, topic=topic)
#     topic.increase_view_count()
