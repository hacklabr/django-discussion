(function(angular){
    'use strict';

    var app = angular.module('discussion', [
        'discussion.controllers',
        'discussion.services',
        'discussion.directives',
        'ngRoute',
        'ui.tinymce',
        'ui.bootstrap',
        'ngFileUpload',
        'ui.select',
        'ngSanitize',
        'ngAnimate',
        'duScroll',
    ]);

    // Set new default values for 'duScroll'
    app.value('duScrollDuration', 1000);
    app.value('duScrollOffset', 100);

    app.config(['$locationProvider', '$routeProvider',
        function config($locationProvider, $routeProvider) {
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
