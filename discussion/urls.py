# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from discussion.views import (
    BasicForumViewSet, CategoryViewSet, CommentFileViewSet, CommentLikeViewSet, CommentViewSet,
    ContentFileViewSet, ForumCreateView, ForumDeleteView, ForumFileViewSet,
    ForumListView, ForumSearchViewSet, ForumUpdateView, ForumView, ForumViewSet,
    TagViewSet, TopicFileViewSet, TopicLikeViewSet, TopicNotificationViewSet,
    TopicPageViewSet, TopicReadViewSet, TopicTypeaheadViewSet, TopicViewSet, ForumPageViewSet
)

from rest_framework import routers


app_name = 'discussion'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'category', BasicForumViewSet)
router.register(r'forum', ForumViewSet) 
router.register(r'basic_forum', BasicForumViewSet)
router.register(r'forum_page', ForumPageViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'topic_page', TopicPageViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'tag', TagViewSet)
router.register(r'topic-notification', TopicNotificationViewSet)
router.register(r'comment_like', CommentLikeViewSet)
router.register(r'comment-file', CommentFileViewSet)
router.register(r'topic_like', TopicLikeViewSet)
router.register(r'forum-file', ForumFileViewSet)
router.register(r'topic-file', TopicFileViewSet)
router.register(r'content-file', ContentFileViewSet)
router.register(r'topic-read', TopicReadViewSet)
router.register(r'search', ForumSearchViewSet)
router.register(r'typeahead', TopicTypeaheadViewSet)

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^$', ForumView.as_view(), name='forum'),
    url(r'^admin/forum-create$', ForumCreateView.as_view(), name='forum-create'),
    url(r'^admin$', ForumListView.as_view(), name='forum-list'),
    url(r'^admin/forum-update/(?P<pk>[-a-zA-Z0-9_]+)$', ForumUpdateView.as_view(), name='forum-update'),
    url(r'^admin/forum-delete/(?P<pk>[-a-zA-Z0-9_]+)$', ForumDeleteView.as_view(), name='forum-delete'),
    url(r'^topic/(?:#(?P<topic_id>[-a-zA-Z0-9_]+))?$', TemplateView.as_view(template_name="forum-topic.html")),
    url(r'^topic/new/', TemplateView.as_view(template_name="forum-new-topic.html")),
    url(r'^forum/embed/$', TemplateView.as_view(template_name="forum-embed.html")),
    url(r'^home/$', RedirectView.as_view(url='/discussion/', permanent=False), name='forum-home'),

    # Templates for Angular components
    url(r'^forum-summary.template.html', TemplateView.as_view(template_name="components/forum-summary.template.html")),
    url(r'^topic-create.template.html', TemplateView.as_view(template_name="components/topic-create.template.html")),
    url(r'^topic-detail.template.html', TemplateView.as_view(template_name="components/topic-detail.template.html")),
]
