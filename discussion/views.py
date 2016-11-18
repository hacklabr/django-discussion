from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils import timezone
from permissions import IsTopicAuthor, IsCommentAuthor

from django.db.models import Q

from discussion.serializers import (CategorySerializer, ForumSerializer, ForumSearchSerializer, TopicSearchSerializer, TopicSerializer, CommentSerializer,
                                    TagSerializer, TopicNotificationSerializer, TopicLikeSerializer,
                                    CommentLikeSerializer, TopicFileSerializer, CommentFileSerializer)
from discussion.models import (Category, Forum, Topic, Comment, Tag, TopicNotification, TopicLike,
                               CommentLike, TopicFile, CommentFile, TopicRead)
from paralapraca.models import AnswerNotification


class CategoryViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.request.user.accounts.all()


class ForumViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(ForumViewSet, self).get_queryset()
        queryset = queryset.order_by('id')
        queryset = queryset.filter(Q(is_public=True) | Q(groups__in=self.request.user.groups.all()))

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class ForumSearchViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Forum.objects.all()
    serializer_class = ForumSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'text',)
    # search_fields = ('title', 'text', 'topics__title', 'topics__content', 'topics__comment__text', )


class TopicTypeaheadViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Topic.objects.all()
    serializer_class = ForumSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', )


class TopicPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class TopicViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, )
    ordering_fields = ('last_activity_at', )
    filter_fields = ('forum', )
    permission_classes = (IsAuthenticated, IsTopicAuthor, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, updated_at=timezone.now())

    def perform_update(self, serializer):
        topic = serializer.save(author=self.request.user, updated_at=timezone.now())

        # Since the topic is being updated, it must be marked as unread for all relevant users
        TopicRead.objects.filter(topic=topic).update(is_read=False)

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the topic that must be shown
        try:
            topic = Topic.objects.get(id=kwargs['pk'])
        except Topic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        topicSer = self.get_serializer(topic)

        # Mark the last notification relative to the current topic-user pair as read
        # The following operation is in a try-except block to account for the unlikely case where the user has never recieved a notification about the current topic. This is possible for new users.
        try:
            notification = TopicNotification.objects.get(topic=topic, user=request.user)
            notification.is_read = True
            notification.save(skip_date=True)
        except TopicNotification.DoesNotExist:
            # There isn't a topic notification associated to the current topic-user pair
            pass

        # Maybe is there an answer notification to mark as read?
        try:
            notification = AnswerNotification.objects.get(topic=topic, user=request.user)
            notification.is_read = True
            notification.save(skip_date=True)
        except AnswerNotification.DoesNotExist:
            pass

        return Response(topicSer.data)

    def get_queryset(self):
        queryset = super(TopicViewSet, self).get_queryset()

        # Test if the queryset must be of activities topics or regular ones
        activity = self.request.query_params.get('activity', None)
        if activity:
            queryset = queryset.filter(forum__forum_type='activity')
            exclude_cur_user = self.request.query_params.get('exclude_cur_user', None)
            if exclude_cur_user:
                queryset = queryset.exclude(author=self.request.user)
        else:
            queryset = queryset.filter(forum__forum_type='discussion')
            queryset = queryset.filter(
                Q(forum__is_public=True) |
                Q(forum__groups__in=self.request.user.groups.all())
            )
            # If there are search fields in the request, do the search
            title = self.request.query_params.get('title', None)
            if title:
                queryset = queryset.filter(title__icontains=title)

        return queryset

    def filter_queryset(self, queryset):

        queryset = super(TopicViewSet, self).filter_queryset(queryset)

        queryset = queryset.distinct()

        limit_to = self.request.query_params.get('limit', None)
        if limit_to:
            queryset = queryset[:int(limit_to)]

        return queryset


class TopicPageViewSet(TopicViewSet):
    pagination_class = TopicPagination


class TopicReadViewSet(viewsets.ModelViewSet):
    queryset = TopicRead.objects.all()
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        topic_read, _ = TopicRead.objects.get_or_create(topic_id=int(request.data['topic']), user=request.user)
        topic_read.is_read = True
        topic_read.save()
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsCommentAuthor, )

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user, updated_at=timezone.now())

        # Since there is a new comment, this topic must be marked as unread for all the relevant users
        TopicRead.objects.filter(topic=comment.topic).update(is_read=False)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user, updated_at=timezone.now())


class TagViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class TopicNotificationViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = TopicNotification.objects.all()
    serializer_class = TopicNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(TopicNotificationViewSet, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).exclude(action='new_activity')

        limit_to = self.request.query_params.get('limit_to', None)
        if limit_to:
            queryset = queryset[:int(limit_to)]
        return queryset


class BaseUserReactionViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class TopicLikeViewSet(BaseUserReactionViewSet):
    """
    """

    queryset = TopicLike.objects.all()
    serializer_class = TopicLikeSerializer
    permission_classes = [IsAuthenticated]


class TopicFileViewSet(viewsets.ModelViewSet):
    queryset = TopicFile.objects.all()
    serializer_class = TopicFileSerializer
    permission_classes = [IsAuthenticated]


class CommentFileViewSet(viewsets.ModelViewSet):
    queryset = CommentFile.objects.all()
    serializer_class = CommentFileSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeViewSet(BaseUserReactionViewSet):
    """
    """

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
