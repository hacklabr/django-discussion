from rest_framework import serializers
from django.contrib.auth import get_user_model
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('password',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1


class BaseTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'edited_at', 'is_hidden', 'slug', 'title', 'content', 'is_private', 'author',
                  'hidden_by', 'tags', 'categories',)
        depth = 1


class ForumSerializer(serializers.ModelSerializer):

    latest_topics = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_private', 'author', 'category', 'latest_topics',)
        depth = 1

    @staticmethod
    def get_latest_topics(obj):
        return BaseTopicSerializer(Topic.objects.all()[:3], many=True).data

class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
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
