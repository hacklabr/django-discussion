# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView

from discussion.views import (CategoryViewSet, ForumViewSet, ForumSearchViewSet, TopicTypeaheadViewSet, TopicViewSet, CommentViewSet, TagViewSet,
                              TopicNotificationViewSet, TopicLikeViewSet, CommentLikeViewSet, TopicFileViewSet, CommentFileViewSet)

from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'category', CategoryViewSet)
router.register(r'forum', ForumViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'tag', TagViewSet)
router.register(r'topic-notification', TopicNotificationViewSet)
router.register(r'comment_like', CommentLikeViewSet)
router.register(r'comment-file', CommentFileViewSet)
router.register(r'topic_like', TopicLikeViewSet)
router.register(r'topic-file', TopicFileViewSet)
router.register(r'search', ForumSearchViewSet)
router.register(r'typeahead', TopicTypeaheadViewSet)

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^$', TemplateView.as_view(template_name="forum.html"), name='forum'),
    url(r'^topic/(?:#(?P<topic_id>[-a-zA-Z0-9_]+))?$', TemplateView.as_view(template_name="forum-topic.html")),
    url(r'^topic/new/', TemplateView.as_view(template_name="forum-new-topic.html")),
]
