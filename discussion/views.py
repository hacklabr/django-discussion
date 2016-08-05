from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import pagination
from rest_framework.response import Response

from django.db.models import Q

from discussion.serializers import (CategorySerializer, ForumSerializer, ForumSearchSerializer, TopicSerializer, CommentSerializer,
                                    TagSerializer, TopicNotificationSerializer, TopicLikeSerializer,
                                    CommentLikeSerializer,)
from discussion.models import (Category, Forum, Topic, Comment, Tag, TopicNotification, TopicLike,
                               CommentLike,)


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
        queryset = queryset.filter(Q(is_public=True) | Q(groups__in=self.request.user.groups.all()))

        return queryset.distinct()


class ForumSearchViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Forum.objects.all()
    serializer_class = ForumSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'text',)
    # search_fields = ('title', 'text', 'topics__title', 'topics__content', 'topics__comment__text', )


class TopicViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, )
    ordering_fields = ('last_activity_at', )
    filter_fields = ('forum', )
    # pagination_class = SimpleLimitPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super(TopicViewSet, self).get_queryset()

        queryset = queryset.filter(
            Q(forum__is_public=True) |
            Q(forum__groups__in=self.request.user.groups.all())
        )

        return queryset

    def filter_queryset(self, queryset):

        queryset = super(TopicViewSet, self).filter_queryset(queryset)

        queryset = queryset.distinct()

        limit_to = self.request.query_params.get('limit', None)
        if limit_to:
            queryset = queryset[:int(limit_to)]

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


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
        queryset = queryset.filter(user=self.request.user)

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


class CommentLikeViewSet(BaseUserReactionViewSet):
    """
    """

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
