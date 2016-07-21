from rest_framework import serializers
from django.contrib.auth import get_user_model
from discussion.models import (Category, Forum, Topic, Comment, Tag, TopicNotification, TopicLike, TopicUse,
                               CommentLike,)
from accounts.serializers import TimtecUserSerializer


class BaseUserSerializer(TimtecUserSerializer):
    pass
    # class Meta:
    #     model = get_user_model()
    #     exclude = ('password',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1


class BaseTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_private', 'author',
                  'hidden_by', 'tags', 'categories', 'count_likes', 'count_uses', 'count_replies', 'last_update',)
        depth = 1


class ForumSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer()
    latest_topics = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_private', 'author', 'category', 'latest_topics',)
        depth = 1

    @staticmethod
    def get_latest_topics(obj):
        return BaseTopicSerializer(Topic.objects.all()[:5], many=True).data


class TopicSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer()

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_private', 'author',
                  'hidden_by', 'tags', 'categories', 'count_likes', 'count_uses', 'forum',)
        depth = 1


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        depth = 1


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        depth = 1


class TopicNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicNotification
        depth = 1


class TopicLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicLike
        depth = 1


class TopicUseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicUse
        depth = 1


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        depth = 1
