from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from discussion.serializers import (CategorySerializer, ForumSerializer, TopicSerializer, CommentSerializer,
                                    TagSerializer, TopicNotificationSerializer, )
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


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


class TopicViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


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
