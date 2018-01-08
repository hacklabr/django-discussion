# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from discussion.views import (CategoryViewSet, ForumViewSet, ForumSearchViewSet, TopicTypeaheadViewSet, TopicViewSet, CommentViewSet, TagViewSet, TopicPageViewSet,
                              TopicNotificationViewSet, TopicLikeViewSet, CommentLikeViewSet, TopicFileViewSet, CommentFileViewSet, ContentFileViewSet, TopicReadViewSet, ForumView,
                              ForumCreateView, ForumListView, ForumUpdateView, ForumDeleteView)

from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'category', CategoryViewSet)
router.register(r'forum', ForumViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'topic_page', TopicPageViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'tag', TagViewSet)
router.register(r'topic-notification', TopicNotificationViewSet)
router.register(r'comment_like', CommentLikeViewSet)
router.register(r'comment-file', CommentFileViewSet)
router.register(r'topic_like', TopicLikeViewSet)
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
    url(r'^home/$', RedirectView.as_view(url='/discussion/', permanent=False), name='forum-home'),
]
