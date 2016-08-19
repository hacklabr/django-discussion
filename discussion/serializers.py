from rest_framework import serializers
from discussion.models import (Category, Forum, Topic, Comment, Tag, TopicNotification, TopicLike,
                               CommentLike, TopicFile, CommentFile)
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
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_public', 'author',
                  'hidden_by', 'tags', 'categories', 'count_likes', 'count_uses', 'count_replies', 'last_activity_at',
                  'forum', )
        depth = 1


class BaseForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'category', )


class ForumSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer(read_only=True)
    latest_topics = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'author', 'category', 'latest_topics', )
        depth = 1

    @staticmethod
    def get_latest_topics(obj):
        return BaseTopicSerializer(Topic.objects.filter(forum=obj).order_by('-last_activity_at')[:5], many=True).data


class BaseCommentSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer(read_only=True)
    user_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment

    def get_user_like(self, obj):
        request = self.context.get("request")
        try:
            return obj.likes.get(user=request.user).id
        except CommentLike.DoesNotExist:
            pass
        return 0


class CommentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentFile


class CommentReplySerializer(BaseCommentSerializer):

    files = CommentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'updated_at', 'slug', 'text', 'author',
                  'hidden_by', 'tags', 'count_likes', 'comment_replies', 'user_like', 'files',)
        depth = 1


class CommentSerializer(BaseCommentSerializer):

    author = BaseUserSerializer(read_only=True)
    comment_replies = CommentReplySerializer(many=True, read_only=True)
    files = CommentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'updated_at', 'slug', 'text', 'author', 'topic',
                  'hidden_by', 'tags', 'count_likes', 'comment_replies', 'user_like', 'parent',
                  'files', )
        # depth = 1


class TopicFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicFile


class TopicSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()
    forum_info = BaseForumSerializer(source='forum', read_only=True)
    files = TopicFileSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_public', 'author',
                  'hidden_by', 'tags', 'categories', 'count_likes', 'count_uses', 'count_replies', 'forum', 'comments',
                  'user_like', 'last_activity_at', 'forum_info', 'files')

    def get_comments(self, obj):
        queryset = obj.comments.filter(parent=None).order_by('-updated_at')
        return CommentSerializer(instance=queryset, many=True, **{'context': self.context}).data

    def get_categories(self, obj):
        return CategorySerializer(instance=obj.categories, many=True, **{'context': self.context}).data

    def get_tags(self, obj):
        return TagSerializer(instance=obj.tags, many=True, **{'context': self.context}).data

    def get_user_like(self, obj):
        request = self.context.get("request")
        try:
            return obj.likes.get(user=request.user).id
        except TopicLike.DoesNotExist:
            return 0


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        depth = 1


class TopicLikeSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = TopicLike


class CommentLikeSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = CommentLike


class TopicNotificationSerializer(serializers.ModelSerializer):

    topic = BaseTopicSerializer(read_only=True)
    comment = BaseCommentSerializer(read_only=True)
    topic_like = TopicLikeSerializer(read_only=True)
    comment_like = CommentLikeSerializer(read_only=True)

    class Meta:
        model = TopicNotification
        depth = 1


class ForumSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'category', 'topics', )
        depth = 1


class TopicSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'title', 'content', 'slug', 'is_public', )
        depth = 1
