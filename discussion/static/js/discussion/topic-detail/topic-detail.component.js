(function() {
    'use strict';
    angular.
        module('topicDetail').
        component('topicDetail', {
            templateUrl: '/discussion/topic-detail.template.html',
            controller: TopicCtrl,
            bindings: {},
        });

    TopicCtrl.$inject = [
        '$scope',
        '$stateParams',
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

    function TopicCtrl ($scope, $stateParams, $sce, $location, $anchorScroll, Forum, Category, Tag, Topic, TopicFile, TopicRead, Comment, TopicLike, CommentLike, CommentFile, CurrentUser, ContentFile) {
        $scope.topic_pinned = false;
        $scope.user = CurrentUser;
        $scope.categories = Category.query();

        $scope.topic = Topic.get({id: $stateParams.topicId}, function(topic){
            // Mark topic as read
            if (topic.categories.length > 0)
                $scope.category_id = $scope.topic.categories[0].id;

            var topic_read = new TopicRead();
            topic_read.topic = topic.id;
            topic_read.is_read = true;
            topic_read.$save();

            //Filter the topics from Forum
            Forum.get({id:$scope.topic.forum}, function(t) {
                $scope.forum_categories = $scope.categories;

                let filteredGroups = t.groups_ids.filter(value => $scope.user.groups_ids.includes(value));
                if(filteredGroups.length > 0) {
                    $scope.topic_pinned = true;
                } else {
                    $scope.topic_pinned = false;
                } 
            }
            );

        }, function(error) {
            $scope.fatal_error = true;
            $scope.error_message = error.data.message;
        });
        

//            uiTinymceConfig.automatic_uploads = true;

//            uiTinymceConfig.images_upload_handler = ContentFile.upload;

        // Prepare for topic editing
//            $scope.forums = Forum.query();
        // $scope.categories = Category.query();
        $scope.tags = Tag.query();
        // angular.copy($scope.topic, $scope.current_topic);
        $scope.update_topic = function() {
            $scope.topic.categories = $scope.category_id;
            var topic_files = $scope.topic.files;
            $scope.topic.$update(function(topic){
                angular.forEach(topic_files, function(topic_file) {
                    if(topic_file instanceof TopicFile){ // Prepare only new files for store in the topic
                      topic_file.topic = topic.id;
                      delete topic_file.file;
                      topic_file.$patch().then(function(comment_file_complete) {
                          topic.files.push(comment_file_complete);
                      });
                    }
                });
                $scope.updating = false;
                // Mark topic as read
                var topic_read = new TopicRead();
                topic_read.topic = topic.id;
                topic_read.is_read = true;
                topic_read.$save();
            });
        };

        $scope.uploadTopicFiles = function (file, topic) {

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
                }, function (evt) {
                    topic.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                });
            }
        };

        // Turn new tags into serializable objects
        $scope.tagTransform = function (newTag) {
            var item = {
                name: newTag.toLowerCase()
             };
             return item;
        };

        $scope.tagExists = function (newTag) {
            for (var tag of $scope.tags)
                if (tag.name.toLowerCase() == newTag)
                    return true;
            return false;
        }

        // Bootstrap functions for new comments and replies
        $scope.new_comment = function(){
            var comment = new Comment();
            comment.topic = $scope.topic;
            return comment;
        };

        $scope.save_comment = function(comment, parent_comment) {
            if (parent_comment) {
                comment.parent = parent_comment.id;
                parent_comment.comment_replies.push(comment);
            } else {
                comment.topic.comments.push(comment);
            }
            // Store files to be saved after the comment
            var files = [];
            angular.copy(comment.files, files);
            delete comment.files;

            // Turn the topic object into an id for JSON parsing
            comment.topic = comment.topic.id;

            // Send the comment data to be saved by the API
            comment.$save().then(function(comment) {
                angular.forEach(files, function(comment_file) {
                    comment_file.comment = comment.id;
                    delete comment_file.file;
                    comment_file.$patch().then(function(comment_file_complete) {
                        comment.files.push(comment_file_complete);
                    });
                });
                //clear variable to prepare for new comment
                comment = $scope.new_comment();
            }, (err) => console.error(err));
        };

        $scope.update_comment = function(changed_comment) {
            var comment_files = changed_comment.files;

            // Get the correct comment instance from the server
            Comment.get({id: changed_comment.id}, function(comment){
              comment.text = changed_comment.text;
              angular.copy(comment, changed_comment);
              comment.$update().then(function(comment) {
                  angular.forEach(comment_files, function(comment_file) {
                        if(comment_file instanceof CommentFile){ // Prepare only new files for store in the topic
                          comment_file.comment = comment.id;
                          delete comment_file.file;
                          comment_file.$patch().then(function(comment_file_complete) {
                              changed_comment.files.push(comment_file_complete);
                          });
                      }
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
        $scope.uploadCommentFiles = function (file, comment) {

            if (file) {
                CommentFile.upload(file).then(function (response) {
                    var comment_file = new CommentFile(response.data);

                    if (comment.files === undefined)
                        comment.files = [];
                    comment.files.push(comment_file);
                    return {location: comment_file.file};
                }, function (response) {
                    if (response.status > 0) {
                        $scope.errorMsg = response.status + ': ' + response.data;
                    }
                }, function (evt) {
                    comment.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
                });
            }
        }

        $scope.get_as_safe_html = function(html_content) {
            return $sce.trustAsHtml(html_content);
        }
    }
})();