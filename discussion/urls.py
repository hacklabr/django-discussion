# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView

from discussion.views import (CategoryViewSet, ForumViewSet, TopicViewSet, CommentViewSet, TagViewSet,
                              TopicNotificationViewSet,)

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet)
router.register(r'forum', ForumViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'tag', TagViewSet)
router.register(r'topic-notification', TopicNotificationViewSet)

urlpatterns = [

    url(r'^api/', include(router.urls)),
    url(r'^forum/', TemplateView.as_view(template_name="forum.html"), name='forum'),
    url(r'^topic/(?:#(?P<topic_id>[-a-zA-Z0-9_]+))?$', TemplateView.as_view(template_name="forum-thread.html")),
    # url(r'^(#/topic/)(?P<topic_id>[-a-zA-Z0-9_]+)$', TemplateView.as_view(template_name="forum-thread.html")),
    # url(r'^(?:#/topic/(?P<topic_id>[-a-zA-Z0-9_]+))$', TemplateView.as_view(template_name="forum-thread.html")),
]