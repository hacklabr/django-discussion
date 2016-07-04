from django.db.models.signals import post_save
from django.dispatch import receiver
from discussion.models import Topic, Comment, CommentHistory, TopicNotification


@receiver(post_save, sender=Topic)
def topic_created_or_updated(sender, **kwargs):
    pass


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
