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


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
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
    topics = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'author', 'category', 'latest_topics', 'forum_type', 'topics', )
        depth = 1

    @staticmethod
    def get_latest_topics(obj):
        return BaseTopicSerializer(Topic.objects.filter(forum=obj).order_by('-last_activity_at')[:5], many=True).data

    def get_topics(self, obj):
        request = self.context.get("request")
        if request:
            queryset = Topic.objects.filter(forum=obj)
            categories = request.query_params.getlist('categories', None)
            if categories:
                queryset = queryset.filter(categories__id__in=categories)
            tags = request.query_params.getlist('tags', None)
            if tags:
                queryset = queryset.filter(tags__id__in=tags)

            # only exec the query if any filter is present
            if categories or tags:
                return BaseTopicSerializer(queryset.order_by('-last_activity_at'), many=True).data
            else:
                return BaseTopicSerializer(queryset.order_by('-last_activity_at')[:5], many=True).data


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

    def create(self, validated_data):
        topic = Topic.objects.create(**validated_data)
        # If categories were specified
        if 'categories' in self.initial_data.keys():
            categories = self.initial_data.pop('categories')
            for cat in categories:
                topic.categories.add(Category.objects.get(id=cat['id']))

        # If tags were specified
        if 'tags' in self.initial_data.keys():
            tags = self.initial_data.pop('tags')
            for tag in tags:
                # Check if it's a new tag
                if 'isTag' in tag.keys():
                    tag = Tag.objects.create(name=tag['name'])
                else:
                    tag = Tag.objects.get(id=tag['id'])
                topic.tags.add(tag)

        return topic

    def update(self, instance, validated_data):
        # Update topic fields
        # import pdb; pdb.set_trace()
        instance.title = self.initial_data['title']
        instance.content = self.initial_data['content']
        instance.forum = Forum.objects.get(id=self.initial_data['forum'])
        instance.updated_at = validated_data['updated_at']

        # Clean current categories
        instance.categories.clear()
        # If categories were specified
        if 'categories' in self.initial_data.keys():
            categories = self.initial_data.pop('categories')
            for cat in categories:
                instance.categories.add(Category.objects.get(id=cat['id']))

        # Clean current tags
        instance.tags.clear()
        # If tags were specified
        if 'tags' in self.initial_data.keys():
            tags = self.initial_data.pop('tags')
            for tag in tags:
                # Check if it's a new tag
                if 'isTag' in tag.keys():
                    tag = Tag.objects.create(name=tag['name'])
                else:
                    tag = Tag.objects.get(id=tag['id'])
                instance.tags.add(tag)

        instance.save()
        return instance

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
