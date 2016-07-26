from django.db.models.signals import post_save
from django.dispatch import receiver
from discussion.models import Topic, Comment, CommentHistory, TopicNotification, TopicLike, TopicUse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, models

@receiver(post_save, sender=Topic)
def topic_created_or_updated(instance, **kwargs):

    # Adjust last_activity_at in Topic
    instance.last_activity_at = instance.updated_at

    User = get_user_model()
    forum = instance.forum

    if forum.is_public == True:
        users = User.objects.all()
    else:
        users = []

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

    # TODO take real group permissions into account when triggering notifications


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


    if not instance.parent: # If the comment is not an answer to another comment
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
