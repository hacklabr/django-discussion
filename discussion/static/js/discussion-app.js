(function(angular){
    'use strict';

    var app = angular.module('discussion', [
        'discussion.controllers',
        'discussion.services',
        'ngRoute',
        'ui.tinymce',
        'ui.bootstrap',
        'ngFileUpload',
    ]);

    app.config(['$resourceProvider', function($resourceProvider) {
          // Don't strip trailing slashes from calculated URLs
          $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);

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
                    controller: 'ForumCtrl'
                }).
                when('/', {
                    templateUrl: 'forum.html',
                    controller: 'ForumCtrl'
                }).
                otherwise('/');
        }
    ]);

})(angular);
