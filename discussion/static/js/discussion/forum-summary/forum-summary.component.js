(function() {
    'use strict';
    angular.
        module('forumSummary').
        component('forumSummary', {
            templateUrl: '/discussion/forum-summary.template.html',
            controller: 'ForumCtrl',
            bindings: {},
        });

    ForumCtrl.$inject = [
        '$scope',
        '$routeParams',
        '$http',
        '$location',
        'Category',
        'Forum',
        'ForumPage',
        'Tag',
        'Topic',
        'TopicPage',
        'CurrentUser'
    ];

    function ForumCtrl ($scope, $routeParams, $http, $location, Category, Forum, ForumPage, Tag, Topic, TopicPage, CurrentUser) {

    }
})();