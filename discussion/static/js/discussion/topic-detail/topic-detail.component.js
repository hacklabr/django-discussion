(function() {
    'use strict';
    angular.
        module('topicDetail').
        component('topicDetail', {
            templateUrl: '/discussion/topic-detail.template.html',
            controller: 'TopicCtrl',
            bindings: {},
        });

    TopicCtrl.$inject = [
        '$scope',
        '$routeParams',
        '$sce',
        '$location',
        '$anchorScroll',
        'Forum',
        'Category',
        'Tag',
        'Topic',
        'TopicFile',
        'TopicRead',
        'Comment',
        'TopicLike',
        'CommentLike',
        'CommentFile',
        'CurrentUser',
        'ContentFile',
    ];

    function TopicCtrl ($scope, $routeParams, $sce, $location, $anchorScroll, Forum, Category, Tag, Topic, TopicFile, TopicRead, Comment, TopicLike, CommentLike, CommentFile, CurrentUser, ContentFile) {

    }
})();