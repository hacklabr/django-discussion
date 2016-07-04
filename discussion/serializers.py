from rest_framework import serializers
from discussion.models import Category, Forum, Topic, Comment, Tag, TopicNotification


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag


class TopicNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicNotification
