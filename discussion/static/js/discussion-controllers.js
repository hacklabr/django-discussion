(function(angular){
    'use strict';
    var app = angular.module('discussion.controllers', ['ngSanitize']);

    app.controller('ForumCtrl', ['$scope', '$routeParams', '$http', 'Forum', 'Topic',
        function ($scope, $routeParams, $http, Forum, Topic) {
            function normalInit() {
                $scope.filters = undefined;
                $scope.forum_search = false;
                $scope.forum_single = false;
                $scope.forums = Forum.query({});
                $scope.latest_topics = Topic.query({
                    limit: 6,
                    ordering: '-last_activity_at',
                    }, function(){
                        $scope.topics_loaded = true;
                    }
                )
            }
            function singleInit() {
                $scope.forum = Forum.get({id: forum_id},function(res){
                    $scope.filters = undefined;
                    $scope.forum_search = false;
                    $scope.forum_single = true;
                    $scope.forums = [];
                    res.latest_topics = Topic.query({
                        limit: 100,
                        forum: forum_id,
                        ordering: '-last_activity_at'}, function(topics){
                            $scope.topics_loaded = true;
                        }
                    );
                    $scope.forums.push(res); // to reuse template's ng-repeat
                },function(err){
                    normalInit();
                });
            }

            var forum_id = $routeParams.forumId;

            if(forum_id) {
                singleInit();
            } else {
                normalInit();
            }

            $scope.getResults = function(txt) {
                if(txt.length > 2) {
                    return $http.get('/discussion/api/typeahead/?search='+txt)
                    .then(function(results){
                        if(results.data.length > 0) {
                            var res = [];
                            results.data.unshift({
                                title:"Sugestões de tópicos",
                                disabled: true
                            });
                            return results.data;
                        }
                    });
                }
            }

            $scope.forumFilter = function(operation,type,filter_obj) {
                if(!$scope.filters) {
                    $scope.filters = {};
                    $scope.filters.categories = []
                    $scope.filters.tags = []
                    $scope.filters_query = {};
                    $scope.filters_query.categories = []
                    $scope.filters_query.tags = []
                }

                if(operation == 'clear') {
                    if(forum_id) {
                        singleInit();
                    } else {
                        normalInit();
                    }
                    return;
                }

                if(type == 'cat') {
                    if(operation == 'add') {
                        if($scope.filters_query.categories.indexOf(filter_obj.id) > -1) {
                            return;
                        }
                        $scope.filters.categories.push(filter_obj);
                        $scope.filters_query.categories.push(filter_obj.id);
                    }
                    else {
                        $scope.filters.categories.splice( $scope.filters.categories.indexOf(filter_obj), 1 );
                        $scope.filters_query.categories.splice( $scope.filters_query.categories.indexOf(filter_obj.id), 1 );
                    }
                }
                else {
                    if(operation == 'add') {
                        if($scope.filters_query.tags.indexOf(filter_obj.id) > -1) {
                            return;
                        }
                        $scope.filters.tags.push(filter_obj);
                        $scope.filters_query.tags.push(filter_obj.id);
                    }
                    else {
                        $scope.filters.tags.splice( $scope.filters.tags.indexOf(filter_obj), 1 );
                        $scope.filters_query.tags.splice( $scope.filters_query.tags.indexOf(filter_obj.id), 1 );
                    }
                }

                if($scope.filters.categories.length + $scope.filters.tags.length === 0) {
                    if(forum_id) {
                        singleInit();
                    } else {
                        normalInit();
                    }
                    return;
                }

                $scope.forums = Forum.query({ // TODO: when single forum, filter only within it
                    categories : $scope.filters_query.categories, //array with cat id's
                    tags : $scope.filters_query.tags //array with tag id's
                }, function(r) {
                    $scope.forum_search = true;
                });
            }
        }
    ]);

    app.controller('NewTopicCtrl', ['$scope', '$window', '$location', 'Forum', 'Topic', 'TopicFile',
        function ($scope,  $window, $location, Forum, Topic, TopicFile) {
            $scope.forums = Forum.query();
            $scope.new_topic = new Topic();
            $scope.save_topic = function() {
                $scope.sending = true;
                // $scope.new_topic.forum = 1;
                var topic_files = $scope.new_topic.files;
                $scope.new_topic.$save(function(topic){
                    angular.forEach(topic_files, function(topic_file) {
                        topic_file.topic = topic.id;
                        delete topic_file.file;
                        topic_file.$patch().then(function(comment_file_complete) {
                            topic.files.push(comment_file_complete);
                        });
                    })
                    var url = '/discussion/topic/#!/topic/'+topic.id;
                    $window.location.href = url;
                });
            }

            $scope.uploadCommentFiles = function (file, topic) {

                if (file) {
                    TopicFile.upload(file).then(function (response) {
                        var comment_file = new TopicFile(response.data);

                        if (topic.files === undefined)
                            topic.files = [];
                        topic.files.push(comment_file);
                        return {location: comment_file.file};
                    }, function (response) {
                        if (response.status > 0) {
                            $scope.errorMsg = response.status + ': ' + response.data;
                        }
                    });
                }
            }
        }
    ]);

    app.controller('TopicCtrl', ['$scope', '$routeParams', 'uiTinymceConfig', 'Forum', 'Topic', 'Comment', 'TopicLike', 'CommentLike', 'CommentFile',
        function ($scope, $routeParams, uiTinymceConfig, Forum, Topic, Comment, TopicLike, CommentLike, CommentFile) {

            $scope.topic = Topic.get({id: $routeParams.topicId});

            uiTinymceConfig.automatic_uploads = true;

            $scope.save_comment = function(topic, parent_comment) {
                var new_comment = new Comment();
                var new_comment_files = [];
                new_comment.topic = topic.id;
                if (parent_comment) {
                    new_comment.parent = parent_comment.id;
                    new_comment.text = parent_comment.new_comment;
                    new_comment_files = parent_comment.new_comment_files;
                    parent_comment.comment_replies.unshift(new_comment);
                } else {
                    new_comment.text = topic.new_comment;
                    topic.show_comment_input = false;
                    new_comment_files = topic.new_comment_files;
                    topic.comments.unshift(new_comment);
                }
                new_comment.$save().then(function(comment) {
                    angular.forEach(new_comment_files, function(comment_file) {
                        comment_file.comment = comment.id;
                        delete comment_file.file;
                        comment_file.$patch().then(function(comment_file_complete) {
                            comment.files.push(comment_file_complete);
                        });
                    });
                });
            };

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

            // uiTinymceConfig.file_browser_callback = function(field_name, url, type, win) {
            //     if(type=='image') {
            //         $('#select-file').click();
            //         console.log('file_browser_callback called!');
            //     }
            // };
            //
            // uiTinymceConfig.images_upload_handler = function (blobInfo, success, failure) {
            //     console.log('images_upload_handler called!');
            // };

            // ng-file-upload
            $scope.uploadCommentFiles = function (file, topic) {

                if (file) {
                    CommentFile.upload(file).then(function (response) {
                        var comment_file = new CommentFile(response.data);

                        if (topic.new_comment_files === undefined)
                            topic.new_comment_files = [];
                        topic.new_comment_files.push(comment_file);
                        return {location: comment_file.file};
                    }, function (response) {
                        if (response.status > 0) {
                            $scope.errorMsg = response.status + ': ' + response.data;
                        }
                    }, function (evt) {
                        // $scope.progress =
                        //     Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                    });
                }
            }

        }
    ]);

})(window.angular);
