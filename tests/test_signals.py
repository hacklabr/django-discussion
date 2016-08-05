#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-discussion
------------

Tests for `django-discussion` models module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from discussion import models
from django.contrib.auth.models import Group
from discussion.models import Topic, Comment, TopicNotification, TopicLike, TopicUse, CommentLike


class TestSignals(TestCase):

    def setUp(self):
        self.george = User.objects.create_user(
            username='george', email='george@asfasdfas.com', password='top_secret')

        self.lorraine = User.objects.create_user(
            username='lorraine', email='lorraine@asfasdfas.com', password='top_secret')

        self.jennifer = User.objects.create_user(
            username='jennifer', email='jennifer@asfasdfas.com', password='top_secret')

        self.brown = User.objects.create_user(
            username='brown', email='brown@asfasdfas.com', password='top_secret')

        self.marty = User.objects.create_user(
            username='marty', email='marty@asfasdfas.com', password='top_secret')

        self.biff = User.objects.create_user(
            username='biff', email='biff@asfasdfas.com', password='top_secret')

        self.category = models.Category.objects.create(
            name='Present',
            description='Where it all begins',
        )

        self.time_travelers = Group.objects.create(name="TimeTravelers")

        self.brown.groups.add(self.time_travelers)
        self.marty.groups.add(self.time_travelers)
        self.jennifer.groups.add(self.time_travelers)

        self.forum = models.Forum.objects.create(author=self.brown, title="Delorean Fans")
        self.forum.groups.add(self.time_travelers)

    def test_post_save_post(self):

        self.trains = models.Topic(
            author=self.brown, forum=self.forum, title="Thoughts about trains?", content="Just thinking aloud")
        self.trains.save()
        notfied_users = [t.user for t in TopicNotification.objects.filter(topic=self.trains).all()]

        # Biff should not have been notified, since he is not a time traveler
        self.assertNotIn(self.biff, notfied_users)

        # Brown should not be notified, since he is the author
        self.assertNotIn(self.brown, notfied_users)

        # Jennifer should be notified, since she is a time traveler
        self.assertIn(self.jennifer, notfied_users)

        public_forum = models.Forum.objects.create(author=self.brown, title="Back to the Future Fans")
        public_forum.is_public = True

        public_topic = models.Topic(
            author=self.biff, forum=public_forum, title="Best movie ever", content="You know it")
        public_topic.save()

        # Everybody, except for the author, should have been notified about the public_topic
        notfied_users = [n.user for n in TopicNotification.objects.filter(topic=public_topic).all()]
        all_other_users = [user for user in User.objects.all() if user != self.biff]
        self.assertEqual(set(all_other_users), set(notfied_users))

    def tearDown(self):
        pass
