#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-discussion
------------

Tests for `django-discussion` models module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from mock import patch
from discussion import models


class TestSignals(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@asfasdfas.com', password='top_secret')

        self.comment = models.Category.objects.create(
            name='Title',
            description='Test text Test text Test text Test text Test text',
        )

        self.forum = models.Forum.objects.create(author=self.user, title="Forum Title")

        self.topic = models.Topic(
            author=self.user, forum=self.forum, title="Topic Title", content="Topic example text")
        self.topic.save()

    def test_post_save_post(self):
        pass

    @patch('discussion.signals.comment_created_or_updated')
    def test_post_save_comment(self, mock):
        comment = models.Comment(text='Test comment', author=self.user, topic=self.topic)
        # comment = models.Comment.objects.create(text='Test comment')
        comment.save()

        # import pdb;pdb.set_trace()

        # Check that your signal was called.
        # self.assertTrue(mock.called)

        # Check that your signal was called only once.
        self.assertEqual(mock.call_count, 1)
        # self.assertQuerysetEqual()

        # self.assertEqual(lion.speak(), 'The lion says "roar"')

    def tearDown(self):
        pass
