(function(angular){
    'use strict';

    var app = angular.module('discussion', [
        'discussion.controllers',
        'discussion.services',
        'discussion.directives',
        'discussion.filters',
        'ngRoute',
        'ui.tinymce',
        'ui.bootstrap',
        'ngFileUpload',
        'ui.select',
        'ngSanitize',
        'ngAnimate',
        'duScroll',
        'LocalStorageModule',
        'shared',
        'djangular'
    ]);

    // Set new default values for 'duScroll'
    app.value('duScrollDuration', 1000);
    app.value('duScrollOffset', 100);

    app.config(['$locationProvider', '$routeProvider', 'localStorageServiceProvider',
        function config($locationProvider, $routeProvider,
            localStorageServiceProvider) {
            localStorageServiceProvider.setPrefix('');
            $locationProvider.hashPrefix('!');

            $routeProvider.
                when('/topic/new/', {
                    templateUrl: 'topic-new.html',
                    controller: 'NewTopicCtrl'
                }).
                when('/topic/:topicId/', {
                    templateUrl: 'topic-detail.html',
                    controller: 'TopicCtrl'
                }).
                when('/forum/embed/', {
                    templateUrl: 'forum-embed.html',
                    controller: 'ForumEmbedCtrl',
                    reloadOnSearch: false
                }).
                when('/forum/:forumId', {
                    templateUrl: 'forum.html',
                    controller: 'ForumCtrl',
                    reloadOnSearch: false
                }).
                when('/', {
                    templateUrl: 'forum.html',
                    controller: 'ForumCtrl',
                    reloadOnSearch: false
                }).
                otherwise('/');
        }
    ]);
})(angular);
