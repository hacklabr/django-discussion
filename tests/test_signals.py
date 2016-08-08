#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-discussion
------------

Tests for `django-discussion` signals module.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from discussion import models
from django.contrib.auth.models import Group
from discussion.models import Topic, Comment, TopicNotification, TopicLike, TopicUse, CommentLike


class TestSignals(TestCase):

    def setUp(self):
        self.user_george = User.objects.create_user(
            username='george', email='george@asfasdfas.com', password='top_secret')

        self.user_lorraine = User.objects.create_user(
            username='lorraine', email='lorraine@asfasdfas.com', password='top_secret')

        self.user_jennifer = User.objects.create_user(
            username='jennifer', email='jennifer@asfasdfas.com', password='top_secret')

        self.user_brown = User.objects.create_user(
            username='brown', email='brown@asfasdfas.com', password='top_secret')

        self.user_marty = User.objects.create_user(
            username='marty', email='marty@asfasdfas.com', password='top_secret')

        self.user_biff = User.objects.create_user(
            username='biff', email='biff@asfasdfas.com', password='top_secret')

        self.category = models.Category.objects.create(
            name='Present',
            description='Where it all begins',
        )

        self.time_travelers = Group.objects.create(name="TimeTravelers")

        self.user_brown.groups.add(self.time_travelers)
        self.user_marty.groups.add(self.time_travelers)
        self.user_jennifer.groups.add(self.time_travelers)

        self.forum = models.Forum.objects.create(author=self.user_brown, title="Delorean Fans")
        self.forum.groups.add(self.time_travelers)

    def test_post_save_post(self):

        self.topic_trains = models.Topic(
            author=self.user_brown, forum=self.forum, title="Thoughts about trains?", content="Just thinking aloud")
        self.topic_trains.save()
        notified_users = [t.user for t in TopicNotification.objects.filter(topic=self.topic_trains, action="new_topic")]

        # Biff should not have been notified, since he is not a time traveler
        self.assertNotIn(self.user_biff, notified_users)

        # Brown should not be notified, since he is the author
        self.assertNotIn(self.user_brown, notified_users)

        # Jennifer should be notified, since she is a time traveler
        self.assertIn(self.user_jennifer, notified_users)

        public_forum = models.Forum.objects.create(author=self.user_brown, title="Back to the Future Fans")
        public_forum.is_public = True

        public_topic = models.Topic(
            author=self.user_biff, forum=public_forum, title="Best movie ever", content="You know it")
        public_topic.save()

        # Everybody, except for the author, should have been notified about the public_topic
        notified_users = [n.user for n in TopicNotification.objects.filter(topic=public_topic, action="new_topic")]
        all_other_users = [user for user in User.objects.all() if user != self.user_biff]
        self.assertEqual(set(all_other_users), set(notified_users))

    def test_post_save_comment(self):

        # Event: new topic is created
        topic = models.Topic(
            author=self.user_brown, forum=self.forum, title="Thoughts about trains?", content="Just thinking aloud")
        topic.save()

        # Event: users react to the topic
        TopicLike.objects.create(topic=topic, user=self.user_marty)
        TopicLike.objects.create(topic=topic, user=self.user_jennifer)
        react_users = [self.user_marty, self.user_jennifer]

        comment = Comment.objects.create(author=self.user_biff, topic=topic, text="Some message")
        notified_users_new_comment = [n.user for n in TopicNotification.objects.filter(topic=topic, comment=comment, action="new_comment")]

        # The comment author should not be notified
        self.assertNotIn(self.user_biff, notified_users_new_comment)

        # Users that reacted to the topic should be notified
        for user in react_users:
            self.assertIn(user, notified_users_new_comment)

        # The topic author should be notified about the last comment made
        self.assertIn(self.user_brown, notified_users_new_comment)

        # Make a new comment
        another_comment = Comment.objects.create(author=self.user_lorraine, topic=topic, text="Some message")

        notified_users_new_comment = [n.user for n in TopicNotification.objects.filter(topic=topic, comment=another_comment, action="new_comment")]

        # The topic author should be notified about the last comment made
        self.assertIn(self.user_brown, notified_users_new_comment)

        # Notify who has already commented ou answered to comments in the same topic
        self.assertIn(self.user_biff, notified_users_new_comment)

        # Don't notify who hasn't interacted at all with this topic
        self.assertNotIn(self.user_george, notified_users_new_comment)

    def test_post_save_topic_reaction(self):
        pass

    def test_post_save_comment_reaction(self):
        pass
        # CommentLike.objects.create(user=self.user_lorraine, comment=comment)
        #
        # notified_users_new_like = [n.user for n in TopicNotification.objects.filter(topic=topic, comment=comment, action="new_reaction_comment")]

    def tearDown(self):
        pass
