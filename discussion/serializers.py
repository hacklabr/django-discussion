from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.db.models import Q

from discussion.models import (Category, Forum, Topic, Comment, Tag, ForumFile,
                               TopicNotification, TopicLike, TopicRead,
                               CommentLike, TopicFile, CommentFile, ContentFile)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
            'first_name',
            'last_name',
            'username',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        depth = 1
        fields = '__all__'


class BaseTopicSerializer(serializers.ModelSerializer):

    read = serializers.SerializerMethodField()
    author = BaseUserSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_public', 'is_pinned', 'author',
                  'hidden_by', 'tags', 'categories', 'comments', 'count_likes', 'count_uses', 'count_replies', 'last_activity_at',
                  'forum', 'read')
        depth = 1

    def get_read(self, obj):
        request = self.context.get("request")
        # If there is a TopicRead instance, return the content of "is_read" field
        try:
            topic_read = TopicRead.objects.get(topic=obj, user=request.user)
            return topic_read.is_read
        except TopicRead.DoesNotExist:
            # If there is no instance, the topic is not read yet
            return False


class BaseForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'category')
        

class ForumFileSerializer(serializers.ModelSerializer):
    """ Serializer to Forum file attachments """
    class Meta:
        model = ForumFile


class ForumSerializer(serializers.ModelSerializer):
    author = BaseUserSerializer(read_only=True)
    topics = serializers.SerializerMethodField()
    files = ForumFileSerializer(many=True, read_only=True)
    groups_ids = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'author', 'category', 'forum_type', 'topics', 'files', 'groups_ids',)
        depth = 1
    
    def get_groups_ids(self, obj):
        groups = obj.groups.all().values_list('id', flat=True)
        return groups

    def get_topics(self, obj):
        request = self.context.get("request")
        if request:
            queryset = obj.topics.all()

            search = request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(content__icontains=search)
                )

            categories = request.query_params.getlist('categories', None)
            if categories:
                queryset = queryset.filter(categories__id__in=categories)
            #tags = request.query_params.getlist('tags', None)
            #if tags:
            #    queryset = queryset.filter(tags__id__in=tags)

            queryset = queryset.select_related('author')
            queryset = queryset.prefetch_related('categories', 'tags', 'forum')

            # only exec the query if any filter is present
            #if categories or tags:
            latest_topics = request.query_params.getlist('latest_topics', None)
            if latest_topics:
                return BaseTopicSerializer(queryset.order_by('-is_pinned', '-last_activity_at')[:5], many=True, **{'context': self.context}).data
            else:
                return BaseTopicSerializer(queryset.order_by('-is_pinned', '-last_activity_at'), many=True, **{'context': self.context}).data


class ForumPageSerializer(ForumSerializer):

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'author', 'category', 'forum_type', 'topics')


class BasicForumSerializer(ForumSerializer):

    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Forum
        fields = ('id', 'category', 'is_public', 'title', 'slug', 'timestamp', 'groups')


class BaseCommentSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer(read_only=True)
    user_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

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
        fields = '__all__'


class CommentReplySerializer(BaseCommentSerializer):

    files = CommentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'updated_at', 'slug', 'text', 'author',
                  'hidden_by', 'tags', 'count_likes', 'comment_replies', 'user_like', 'files',)
        depth = 1


class CommentSerializer(BaseCommentSerializer):

    author = BaseUserSerializer(read_only=True)
    comment_replies = serializers.SerializerMethodField()
    files = CommentFileSerializer(many=True, read_only=True)

    def get_comment_replies(self, obj):
        queryset = obj.comment_replies.order_by('created_at')
        return CommentSerializer(instance=queryset, many=True, **{'context': self.context}).data

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'updated_at', 'slug', 'text', 'author', 'topic',
                  'hidden_by', 'tags', 'count_likes', 'comment_replies', 'user_like', 'parent',
                  'files', )
        # depth = 1


class TopicFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicFile
        fields = '__all__'


class ContentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentFile
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):

    author = BaseUserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()
    forum_info = BaseForumSerializer(source='forum', read_only=True)
    files = TopicFileSerializer(many=True, read_only=True)
    read = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_public', 'is_pinned', 'author',
                  'hidden_by', 'tags', 'categories', 'count_likes', 'count_uses', 'count_replies', 'forum', 'comments',
                  'user_like', 'last_activity_at', 'forum_info', 'files', 'read')

    def create(self, validated_data):
        request = self.context.get("request")

        topic = Topic.objects.create(**validated_data)
        # If categories were specified
        if 'categories' in self.initial_data.keys():
            categories = self.initial_data.pop('categories')
            for cat in categories:
                if cat != None:
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

        # If is_pinned is specified and the user belongs to one of the forum groups
        groups = Group.objects.filter(user__id=request.user.id, foruns__id=self.initial_data['forum'])

        if 'is_pinned' in self.initial_data.keys() and groups.exists():
            topic.is_pinned  = True
            topic.save()
       
        return topic

    def update(self, instance, validated_data):
        request = self.context.get("request")

        # Update topic fields
        instance.title = self.initial_data['title']
        instance.content = self.initial_data['content']
        instance.forum = Forum.objects.get(id=self.initial_data['forum'])

        # Clean current categories
        instance.categories.clear()
        # If categories were specified
        if 'categories' in self.initial_data.keys():
            categories = self.initial_data.pop('categories')
            if categories:
                instance.categories.add(Category.objects.get(id=categories))

        # Clean current tags
        instance.tags.clear()
        # If tags were specified
        if 'tags' in self.initial_data.keys():
            tags = self.initial_data.pop('tags')
            for tag in tags:
                # Check if it's a new tag
                if 'isTag' in tag.keys():
                    if not Tag.objects.filter(name=tag['name'].lower()).exists():
                        tag = Tag.objects.create(name=tag['name'].lower())
                    else:
                        tag = Tag.objects.get(name=tag['name'].lower())
                else:
                    tag = Tag.objects.get(id=tag['id'])
                instance.tags.add(tag)

        # If is_pinned were specified and the user belongs to one of the forum groups
        groups = Group.objects.filter(user__id=request.user.id, foruns__id=self.initial_data['forum'])
        if 'is_pinned' in self.initial_data.keys() and groups.exists():
            pin = self.initial_data.pop('is_pinned')
            if pin:
                instance.is_pinned = True
            else:
                instance.is_pinned = False

        instance.save()
        return instance

    def get_comments(self, obj):
        queryset = obj.comments.filter(parent=None).order_by('created_at')
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

    def get_read(self, obj):
        request = self.context.get("request")
        # If there is a TopicRead instance, return the content of "is_read" field
        try:
            topic_read = TopicRead.objects.get(topic=obj, user=request.user)
            return topic_read.is_read
        except TopicRead.DoesNotExist:
            # If there is no instance, the topic is not read yet
            return False


class SimpleTopicSerializer(BaseTopicSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'created_at', 'updated_at', 'is_hidden', 'slug', 'title', 'content', 'is_public', 'author',
                  'hidden_by', 'categories', 'count_likes', 'count_uses', 'count_replies', 'last_activity_at',
                  'read', 'is_pinned')
        depth = 1


class TopicLikeSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = TopicLike
        fields = '__all__'


class CommentLikeSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = '__all__'


class TopicNotificationSerializer(serializers.ModelSerializer):

    topic = BaseTopicSerializer(read_only=True)
    comment = BaseCommentSerializer(read_only=True)
    topic_like = TopicLikeSerializer(read_only=True)
    comment_like = CommentLikeSerializer(read_only=True)

    class Meta:
        model = TopicNotification
        depth = 1
        fields = '__all__'


class ForumSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = ('id', 'title', 'text', 'slug', 'timestamp', 'is_public', 'category', 'topics', )
        depth = 1


class TopicSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'title', 'content', 'slug', 'is_public', 'is_pinned')
        depth = 1
