(function(angular){
    'use strict';
    var app = angular.module('discussion.controllers', ['ngSanitize']);

    app.controller('ForumCtrl', ['$scope', 'Forum', 'Topic',
        function ($scope, Forum, Topic) {
            $scope.forums = Forum.query({});
            $scope.latest_topics = Topic.query({limit: 6, ordering: 'updated_at'})
        }
    ]);

    app.controller('TopicCtrl', ['$scope', '$location', 'Forum', 'Topic', 'TopicLike', 'CommentLike',
        function ($scope, $location, Forum, Topic, TopicLike, CommentLike) {
            var topic_id = $location.hash();
            $scope.topic = Topic.get({id: topic_id})

            $scope.topic_like = function(topic) {
                if (topic.user_like) {
                    TopicLike.delete({id:topic.user_like});
                    topic.user_like = 0;
                    topic.count_likes -=1;
                } else {
                    // Change this before promisse so the user sees the action take effect.
                    topic.user_like = -1;

                    TopicLike.save({topic:topic.id}, function(topic_like){
                        topic.user_like = topic_like.id;
                    });
                    topic.count_likes +=1
                }
            };

            $scope.comment_like = function(comment) {
                if (comment.user_like) {
                    CommentLike.delete({id:comment.user_like});
                    comment.user_like = 0;
                    comment.count_likes -=1;
                } else {
                    // Change this before promisse so the user sees the action take effect.
                    comment.user_like = -1;

                    CommentLike.save({comment:comment.id}, function(comment_like){
                        comment.user_like = comment_like.id;
                    });
                    comment.count_likes +=1
                }
            };

        }
    ]);

})(window.angular);
