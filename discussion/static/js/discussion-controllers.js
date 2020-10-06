(function(angular){
    'use strict';
    var app = angular.module('discussion.controllers', ['ngSanitize']);

    app.controller('ForumCtrl', ['$scope', '$routeParams', '$http', '$location', 'Category', 'Forum', 'ForumPage', 'Tag', 'Topic', 'TopicPage', 'CurrentUser', 'UserAccess',
        function ($scope, $routeParams, $http, $location, Category, Forum, ForumPage, Tag, Topic, TopicPage, CurrentUser, UserAccess) {

            const forum_id = $routeParams.forumId;
            $scope.user = CurrentUser;

            $scope.forum = {}
            $scope.topics = {}
            $scope.search = {txt:""}
            // Pagination Params
            $scope.forum_pages_max_number = 20;
            $scope.forum_topics_page = 20;
            $scope.forum.page_size = 20;
            $scope.forum.current_page = 1

            if(forum_id) {
                singleInit();
            } else {
                normalInit();
            }

            function singleInit() {
                Forum.get({id: forum_id}, (forum) => {
                    $scope.filters = undefined;
                    $scope.forum_search = false;
                    $scope.forum_single = true;
                    $scope.forums = [];
                    $scope.forum = forum;
                    $scope.topics.current_page = 1;
                    $scope.forum.page = TopicPage.get({
                        page: 1,
                        page_size: $scope.forum_topics_page,
                        forum: forum_id,
                        ordering: '-last_activity_at'},
                        function(page){
                            $scope.forum.topics = page.results;
                            $scope.forum_topics_total = page.count;
                            $scope.topics_loaded = true;
                        },
                        function(err){
                            console.log("Erro ao carregar os tópicos");
                        }
                    );
                    $scope.forums.push(forum); // to reuse template's ng-repeat
                },function(err){
                    normalInit();
                });
            }

            function normalInit() {
                // Log this access
                (new UserAccess({ area: 'forums' })).$save();

                $scope.filters = {};
                $scope.forum_single = false;
                const categoriesParams = $routeParams['categories'];
                const tagParams = $routeParams['tags']

                if(categoriesParams || tagParams) {
                    if(categoriesParams) {
                        if(typeof categoriesParams === 'string' || typeof categoriesParams === 'number')
                            $scope.filters.categories = [categoriesParams];
                        else
                            $scope.filters.categories = categoriesParams;

                        $scope.filters.categories = $scope.filters.categories.map(function(cat) {
                            return angular.fromJson(cat);
                        });
                    }
                    else {
                        $scope.filters.categories = [];
                    }
                    if(tagParams) {
                        if(typeof tagParams === 'string' || typeof tagParams === 'number')
                            $scope.filters.tags = [tagParams];
                        else
                            $scope.filters.tags = tagParams;
                        $scope.filters.tags = $scope.filters.tags.map(function(tag) {
                            return angular.fromJson(tag);
                        });
                    }
                    else {
                        $scope.filters.tags = [];
                    }
                    $scope.forum_search = true;
                }
                else {
                    $scope.filters.categories = [];
                    $scope.filters.tags = [];
                    $scope.forum_search = false;
                }

                $scope.forums = ForumPage.get({
                    search: $scope.current_search,  // if there is a search in progress, keep it
                    page: $scope.forum.current_page,
                    page_size: $scope.forum.page_size,
                }, (response) => {
                    $scope.forums = response.results
                    $scope.forum.total_forum_items = response.count
                    $scope.forum.max_size = response.length
                    $scope.forum_page_loaded = response.$resolved;
                    $scope.forum.has_next_page = (response.next !== null || response.previous !== null)
                });
                $scope.latest_topics = Topic.query({
                    limit: 6,
                    ordering: '-last_activity_at',
                    }, function(){
                        $scope.topics_loaded = true;
                    }
                );
            }


            // Pagination controls
            $scope.topicPageChanged = function(){
              $scope.forum.page = TopicPage.get({
                  search: $scope.current_search,  // if there is a search in progress, keep it
                  page: $scope.topics.current_page,
                  page_size: $scope.forum_topics_page,
                  forum: forum_id,
                  ordering: '-last_activity_at'},
                  function(page){
                      $scope.forum.topics = page.results;
                      $scope.topics_loaded = true;
                  },
                  function(err){
                      console.log("Erro ao carregar os tópicos");
                  }
              );
            };
            $scope.forumPageChanged = () => {
                $scope.forums = ForumPage.get({
                    search: $scope.current_search,  // if there is a search in progress, keep it
                    page: $scope.forum.current_page,
                    page_size: $scope.forum.page_size
                }, (response) => {
                    $scope.forums = response.results
                    $scope.forum.total_forum_items = response.count
                    $scope.forum.max_size = response.length
                    $scope.forum_page_loaded = response.$resolved;
                });
              };

            $scope.getResults = function(txt) {
                $scope.current_search = txt;
                TopicPage.get({
                    search: txt,
                    page: 1,
                    page_size: $scope.forum_topics_page,
                    ordering: '-last_activity_at',
                    ignoreLoadingBar: true},
                    function(page){
                        $scope.forums = [];
                        $scope.forum.title = "Resultados de busca";
                        $scope.topics.current_page = 1;
                        $scope.forum.topics = page.results;
                        $scope.forum_topics_total = page.count;
                        $scope.topics_loaded = true;

                        $scope.filters = undefined;
                        $scope.forum_search = true;
                        $scope.forum_single = false;
                        $scope.forums.push($scope.forum); // to reuse template's ng-repeat

                    }, function(err){
                        normalInit();
                    });
            }

            function clear_filters() {
                $scope.filters = {};
                $scope.filters.categories = [];
                $scope.filters.tags = [];
            }

            $scope.clear_search = () => {
                $scope.forum_search = false;
                $scope.current_search = "";
                $scope.forums = {}
                $scope.topics_loaded = false;
                $scope.search = {txt:""}
                normalInit()
            }

            function set_route() {
                var new_url = '#!/';
                if (forum_id)
                    new_url += forum_id;
                var plain_url = true;
                for(var i = 0; i < $scope.filters.categories.length; i++) {
                    if (plain_url)
                        new_url += '?categories=' + angular.toJson($scope.filters.categories[i]);
                    else
                        new_url += '&categories=' + angular.toJson($scope.filters.categories[i]);
                    plain_url = false;
                }
                for(var i = 0; i < $scope.filters.tags.length; i++) {
                    if (plain_url)
                        new_url += '?tags=' + angular.toJson($scope.filters.tags[i]);
                    else
                        new_url += '&tags=' + angular.toJson($scope.filters.tags[i]);
                    plain_url = false;
                }
                window.location.hash = new_url;
            }

            $scope.forumFilter = function(operation, type, filter_obj) {

                if(!$scope.filters) {
                    $scope.filters = {};
                    $scope.filters.categories = []
                    $scope.filters.tags = []
                }

                if(operation == 'clear') {
                    clear_filters();
                }

                if(type === 'cat') {
                    if(operation === 'add') {
                        $scope.filters.categories.some(obj => obj.name === filter_obj.name) ?
                            console.log('already filtering by this category') :
                            $scope.filters.categories.push(filter_obj);
                    }
                    else {
                        $scope.filters.categories.splice( $scope.filters.categories.indexOf(filter_obj), 1 );
                    }
                }
                else {
                    if(operation === 'add') {
                        $scope.filters.tags.some(obj => obj.name === filter_obj.name) ?
                            console.log('already filtering by this tag') :
                            $scope.filters.tags.push(filter_obj);
                    }
                    else {
                        $scope.filters.tags.splice( $scope.filters.tags.indexOf(filter_obj), 1 );
                    }
                }

                if($scope.filters.categories.length + $scope.filters.tags.length === 0) {
                    clear_filters();
                }

                set_route();

                $scope.forums = Forum.query({ // TODO: when single forum, filter only within it
                    categories : $scope.filters.categories.map(function(el) {
                        return el.id;
                    }), //array with cat id's
                    tags : $scope.filters.tags.map(function(el) {
                        return el.id;
                    }) //array with tag id's
                }, function(r) {
                    $scope.forum_search = true;
                });
            }
        }
    ]);

    app.controller('NewTopicCtrl', ['$scope', '$window', '$location', 'Forum', 'BasicForum', 'Topic', 'TopicFile', 'Category', 'Tag', 'ContentFile',
//    'uiTinymceConfig',
        function ($scope,  $window, $location, Forum, BasicForum, Topic, TopicFile, Category, Tag, ContentFile,
//        uiTinymceConfig
        ) {
            $scope.selected_forum = '';
            $scope.forums = BasicForum.query();
            $scope.categories = Category.query();
            $scope.tags = Tag.query();
            $scope.new_topic = new Topic();

//            uiTinymceConfig.images_upload_handler = ContentFile.upload;

            $scope.save_topic = function() {
                $scope.sending = true;
                $scope.new_topic.forum = $scope.selected_forum.id;
                $scope.new_topic.categories = [$scope.category];
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

            $scope.show_errors = false;
            $scope.validate = function(valid) {
                $scope.show_errors = true;
                if(!valid) {
                    setTimeout(function() {
                        $('html, body').animate({
                          scrollTop: $('#errors-list').position().top
                        }, 500);
                    }, 100);
                }
            }

            // Turn new tags into serializable objects
            $scope.tagTransform = function (newTag) {
                var item = {
                    name: newTag.toLowerCase()
                 };
                 return item;
            };

            $scope.new_topic.tags = [];
            $scope.tagExists = function (newTag) {
                for (var tag of $scope.tags)
                    if (tag.name.toLowerCase() == newTag)
                        return true;
                return false;
            }

            $scope.filter_categories = function(){
                $scope.list_categories = $scope.selected_forum.category;
            }

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
        }
    ]);

    app.controller('TopicCtrl', ['$scope', '$routeParams', '$sce', '$location', '$anchorScroll',
//    'uiTinymceConfig',
    'Forum', 'Category', 'Tag', 'Topic', 'TopicFile', 'TopicRead', 'Comment', 'TopicLike', 'CommentLike', 'CommentFile', 'CurrentUser', 'ContentFile',
        function ($scope, $routeParams, $sce, $location, $anchorScroll, 
//        uiTinymceConfig,
        Forum, Category, Tag, Topic, TopicFile, TopicRead, Comment, TopicLike, CommentLike, CommentFile, CurrentUser, ContentFile) {

            $scope.topic = Topic.get({id: $routeParams.topicId}, function(topic){
                // Mark topic as read
                if (topic.categories.length > 0)
                    $scope.category_id = $scope.topic.categories[0].id;

                var topic_read = new TopicRead();
                topic_read.topic = topic.id;
                topic_read.is_read = true;
                topic_read.$save();

                //Filter the topics from Forum
                Forum.get({id:$scope.topic.forum}, function(t) {
                    $scope.forum_categories = t.category;
                }
                );

            }, function(error) {
                $scope.fatal_error = true;
                $scope.error_message = error.data.message;
            });
            $scope.user = CurrentUser;

//            uiTinymceConfig.automatic_uploads = true;

//            uiTinymceConfig.images_upload_handler = ContentFile.upload;

            // Prepare for topic editing
            $scope.forums = Forum.query();
            $scope.categories = Category.query();
            $scope.tags = Tag.query();
            angular.copy($scope.topic, $scope.current_topic);
            $scope.update_topic = function() {
                $scope.topic.categories = $scope.categories.filter(function(cat) {
                    return cat.id == $scope.category_id;
                });
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
    ]);

    app.controller('ForumEmbedCtrl', ['$scope', 'Topic',
        function($scope, Topic) {
            $scope.latest_topics = Topic.query({limit: 8, ordering: '-last_activity_at'})
        }
    ]);

})(window.angular);
