(function(angular){
    'use strict';
    var app = angular.module('discussion.controllers', ['ngRoute']);

    app.controller('ForumCtrl', ['$scope', 'Forum', 'Topic',
        function ($scope, Forum, Topic) {
            $scope.forums = Forum.query({});
            $scope.latest_topics = Topic.query({limit: 6, ordering: 'updated_at'})
        }
    ]);

    app.controller('TopicCtrl', ['$scope', '$location', 'Forum', 'Topic',
        function ($scope, $location, Forum, Topic) {
            var topic_id = $location.hash();
            $scope.topic = Topic.get({id: topic_id})
        }
    ]);

})(window.angular);
