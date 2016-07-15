from rest_framework import serializers
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        depth = 1


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
