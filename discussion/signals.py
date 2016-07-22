from django.db.models.signals import post_save
from django.dispatch import receiver
from discussion.models import Topic, Comment, CommentHistory, TopicNotification
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, models


@receiver(post_save, sender=Topic)
def topic_created_or_updated(instance, **kwargs):

    User = get_user_model()
    forum = instance.forum

    if forum.is_public == True:
        users = User.objects.all()
    else:
        users = []

    for person in users:
        # Create the New Topic notification for appropriate users
        TopicNotification.objects.create(
            user=person,
            topic=instance,
            action='new_topic',
        )


    # TODO take real group permissions into account when triggering notifications


@receiver(post_save, sender=Comment)
def comment_created_or_updated(instance, **kwargs):

    TopicNotification.objects.create(
        user=instance.author, topic=instance.topic, comment=instance, action='comment')

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
