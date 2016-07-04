# -*- coding: utf-8 -*-
from django.conf.urls import url, include

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

    ]
