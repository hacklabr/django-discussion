from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.views.generic.base import TemplateView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from braces import views

from datetime import datetime

from .serializers import (BasicForumSerializer, CategorySerializer, ForumSerializer, ForumSearchSerializer, TopicSearchSerializer,
                                    TopicSerializer, CommentSerializer, ContentFileSerializer,
                                    TagSerializer, TopicNotificationSerializer, TopicLikeSerializer, ForumFileSerializer,
                                    CommentLikeSerializer, TopicFileSerializer, CommentFileSerializer, ForumPageSerializer)
from .models import (Category, Forum, Topic, Comment, Tag, TopicNotification, TopicLike,
                               CommentLike, TopicFile, CommentFile, ContentFile, TopicRead, ForumFile)
from courses.models import Course, Forum

from .forms import ForumForm
from .permissions import IsTopicAuthor, IsCommentAuthor, IsForumAuthor

class ForumView(TemplateView):
    template_name = 'forum.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        return context


class ForumCourseView(views.LoginRequiredMixin, TemplateView):
    template_name = 'forum-course.html'

    def get_context_data(self, **kwargs):
        context = super(ForumCourseView, self).get_context_data(**kwargs)
        course = Course.objects.get(slug=context['slug'])
        context['course'] = course
        return context

class ForumTopicView(views.LoginRequiredMixin, TemplateView):
    template_name = 'forum-course-topic.html'

    def get_context_data(self, **kwargs):
        context = super(ForumTopicView, self).get_context_data(**kwargs)
        course = Course.objects.get(slug=context['slug'])
        context['course'] = course
        return context

class ForumNewTopicView(views.LoginRequiredMixin, TemplateView):
    template_name = 'forum-course-new-topic.html'

    def get_context_data(self, **kwargs):
        context = super(ForumNewTopicView, self).get_context_data(**kwargs)
        course = Course.objects.get(slug=context['slug'])
        context['course'] = course
        return context


class ForumCreateView(views.LoginRequiredMixin,
                      views.StaffuserRequiredMixin,
                      CreateView):
    template_name = 'forum_create_form.html'
    success_url = reverse_lazy('discussion:forum-list')
    form_class = ForumForm

    def form_valid(self, form):
        form.author = self.request.user
        return super(ForumCreateView, self).form_valid(form)


class ForumListView(views.LoginRequiredMixin,
                    views.StaffuserRequiredMixin,
                    ListView):
    model = Forum
    template_name = 'forum-list.html'


    def get_queryset(self):
        queryset = super(ForumListView, self).get_queryset()
        
        queryset = queryset.filter(
            Q(forum_type='discussion') | (Q(forum_type='course') & Q(course=None)),
        )

        return queryset


class ForumUpdateView(views.LoginRequiredMixin,
                      views.StaffuserRequiredMixin,
                      UpdateView):
    model = Forum
    form_class = ForumForm

    template_name = 'forum_update_form.html'
    success_url = reverse_lazy('discussion:forum-list')


class ForumDeleteView(views.LoginRequiredMixin,
                      views.StaffuserRequiredMixin,
                      DeleteView):
    model = Forum
    template_name = 'forum_delete_form.html'
    success_url = reverse_lazy('discussion:forum-list')


class CategoryViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    # def get_queryset(self):
    #     return self.request.user.accounts.all()


class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class CategoryPageViewSet(CategoryViewSet):
    pagination_class = CategoryPagination

    def get_queryset(self):
        queryset = super(CategoryPageViewSet, self).get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search))

        return queryset


class ForumViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]
    filter_fields = ('forum_type',)

    def get_queryset(self):
        queryset = super(ForumViewSet, self).get_queryset()

        queryset = queryset.order_by('id')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(Q(is_public=True) | Q(groups__in=self.request.user.groups.all()))

        # Remove Foruns of type course with no course associated, 
        # in draft or that has not started
        now = datetime.now().date()
        queryset = queryset.exclude(
            Q(forum_type='course') & (
                Q(course=None) |
                Q(course__status='draft') |
                Q(course__start_date__gt=datetime.now().date())
            )
        )

        # Remove foruns of type activity, we don't want then on any user
        # visible list, only inside its specific activity
        queryset = queryset.exclude(
            Q(forum_type='activity'),
        )

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(topics__title__icontains=search) |
                Q(topics__content__icontains=search)
            )

        queryset = queryset.distinct()
        queryset = queryset.select_related('author')
        return queryset.prefetch_related('topics', 'category')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class BasicForumViewSet(ForumViewSet):
    """
    """
    queryset = Forum.objects.all()
    serializer_class = BasicForumSerializer
    permission_classes = [IsAuthenticated]


class ForumPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ForumPageViewSet(ForumViewSet):
    pagination_class = ForumPagination
    serializer_class = ForumPageSerializer


class ForumSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """

    queryset = Forum.objects.all()
    serializer_class = ForumSearchSerializer
    permission_classes = [IsAuthenticated, IsForumAuthor]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'text',)
    # search_fields = ('title', 'text', 'topics__title', 'topics__content', 'topics__comment__text', )


class TopicTypeaheadViewSet(viewsets.ReadOnlyModelViewSet):
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

    queryset = Topic.objects.all().order_by('-is_pinned', '-last_activity_at')
    serializer_class = TopicSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, )
    ordering_fields = ('last_activity_at')
    filter_fields = ('forum', )
    permission_classes = (IsTopicAuthor, IsAuthenticated, )
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, is_pinned=False)

    def perform_update(self, serializer):
        topic = serializer.save()

        # Since the topic is being updated, it must be marked as unread for all relevant users
        TopicRead.objects.filter(topic=topic).update(is_read=False)

    def retrieve(self, request, *args, **kwargs):

        topic = self.get_object()

        topicSer = self.get_serializer(topic)

        # Mark the last notification relative to the current topic-user pair as read
        # The following operation is in a try-except block to account for the unlikely
        # case where the user has never recieved a notification about the current topic,
        # this is possible for new users.
        try:
            notifications = TopicNotification.objects.filter(topic=topic, user=request.user)
            for notification in notifications:
                notification.is_read = True
                notification.save(skip_date=True)
        except TopicNotification.DoesNotExist:
            # There isn't a topic notification associated to the current topic-user pair
            pass

        return Response(topicSer.data)

    def get_queryset(self):
        queryset = super(TopicViewSet, self).get_queryset()

        # Only ilter if its a list, case when pk arg is not present 
        if not self.kwargs.get('pk', False):
            # Test if the queryset must be of activities topics or regular ones
            activity = self.request.query_params.get('activity', None)
            if activity:
                queryset = queryset.filter(forum__forum_type='activity')
                exclude_cur_user = self.request.query_params.get('exclude_cur_user', None)
                if exclude_cur_user:
                    queryset = queryset.exclude(author=self.request.user)
            else:
                queryset = queryset.filter(forum__forum_type__in=['discussion', 'course'])
                if not self.request.user.is_superuser:
                    queryset = queryset.filter(
                        Q(forum__is_public=True) |
                        Q(forum__groups__in=self.request.user.groups.all())
                    )

            # If there are search fields in the request, do the search
            search = self.request.query_params.get('search', None)
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(content__icontains=search) |
                    Q(tags__name__icontains=search) |
                    Q(categories__name__icontains=search))

            category = self.request.query_params.get('category', None)
            if category:
                queryset = queryset.filter(Q(categories__id=category))

            tag = self.request.query_params.get('tag', None)
            if tag:
                queryset = queryset.filter(Q(tags__id=tag))

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
        comment = serializer.save(author=self.request.user)

        # Since there is a new comment, this topic must be marked as unread for all the relevant users
        TopicRead.objects.filter(topic=comment.topic).update(is_read=False)


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


class ForumFileViewSet(viewsets.ModelViewSet):
    queryset = ForumFile.objects.all()
    serializer_class = ForumFileSerializer
    permission_classes = [IsAuthenticated]
    filter_fields = ('forum', )

class TopicFileViewSet(viewsets.ModelViewSet):
    queryset = TopicFile.objects.all()
    serializer_class = TopicFileSerializer
    permission_classes = [IsAuthenticated]


class CommentFileViewSet(viewsets.ModelViewSet):
    queryset = CommentFile.objects.all()
    serializer_class = CommentFileSerializer
    permission_classes = [IsAuthenticated]


class ContentFileViewSet(viewsets.ModelViewSet):
    queryset = ContentFile.objects.all()
    serializer_class = ContentFileSerializer
    permission_classes = [IsAuthenticated]


class CommentLikeViewSet(BaseUserReactionViewSet):
    """
    """

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
