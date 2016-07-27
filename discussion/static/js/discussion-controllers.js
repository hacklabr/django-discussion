(function(angular){
    'use strict';
    var app = angular.module('discussion.controllers', ['ngSanitize']);

    app.controller('ForumCtrl', ['$scope', 'Forum', 'Topic',
        function ($scope, Forum, Topic) {
            $scope.forums = Forum.query({});
            $scope.latest_topics = Topic.query({limit: 6, ordering: 'updated_at'})
        }
    ]);

    app.controller('TopicCtrl', ['$scope', '$location', 'Forum', 'Topic', 'Comment', 'TopicLike', 'CommentLike',
        function ($scope, $location, Forum, Topic, Comment, TopicLike, CommentLike) {
            var topic_id = $location.hash();
            $scope.topic = Topic.get({id: topic_id})

            $scope.tinymceOptions = {
                inline: false,
                menubar: false,
                plugins : 'advlist autolink link image lists charmap print preview',
                toolbar: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
                skin: 'lightgray',
                theme : 'modern',
                language: 'pt_BR',
                language_url : '/static/vendor/tinymce/langs/pt_BR.js',
            };

            $scope.save_comment = function(topic, parent_comment) {
                var new_comment = new Comment();
                new_comment.topic = topic.id;
                if (parent_comment) {
                    new_comment.parent = parent_comment.id;
                    new_comment.text = parent_comment.new_comment;
                    parent_comment.comment_replies.unshift(new_comment);
                } else {
                    new_comment.text = topic.new_comment;
                    topic.show_comment_input = false;
                    topic.comments.unshift(new_comment);
                }

                new_comment.$save();

//                Comment.save(comment_data, function(new_comment){
//                    topic.comments
//                });
            }

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
