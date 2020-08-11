(function() {
    'use strict';
    angular.
        module('topicCreate').
        component('topicCreate', {
            templateUrl: '/discussion/topic-create.template.html',
            controller: 'NewTopicCtrl',
            bindings: {},
        });

    NewTopicCtrl.$inject = [
        '$scope',
        '$window',
        '$location',
        'Forum',
        'Topic',
        'TopicFile',
        'Category',
        'Tag',
        'ContentFile',
    ];

    function NewTopicCtrl ($scope,  $window, $location, Forum, Topic, TopicFile, Category, Tag, ContentFile) {

    }
})();