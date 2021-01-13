(function() {
    'use strict';
    angular.
        module('topicCreate').
        component('topicCreate', {
            templateUrl: '/discussion/topic-create.template.html',
            controller: NewTopicCtrl,
            bindings: {
                forum: '<',
            },
        });

    NewTopicCtrl.$inject = [
        '$scope',
        '$state',
        'Forum',
        'Topic',
        'TopicFile',
        'Category',
        'Tag',
        'ContentFile',
        'CurrentUser',
    ];

    function NewTopicCtrl ($scope, $state, Forum, Topic, TopicFile, Category, Tag, ContentFile, CurrentUser) {
        $scope.categories = Category.query();
        $scope.tags = Tag.query();
        $scope.new_topic = new Topic();
        $scope.pinned = false;

        $scope.user = CurrentUser;

        var ctrl = this;

        this.$onInit = function() {
            // If there is a "crtl.forum", change how "forums" is initialized
            if (ctrl.forum) {
                $scope.forums = [ctrl.forum]
                $scope.new_topic.forum = ctrl.forum.id;

                $scope.filter_categories();
                $scope.disable_forum_selection = true;
            } else {
                // Otherwise, initialize forums normally
                $scope.forums = Forum.query();
            }
        }

        // uiTinymceConfig.images_upload_handler = ContentFile.upload;

        $scope.save_topic = function() {
            $scope.sending = true;
            $scope.new_topic.categories = [$scope.category];
            var topic_files = $scope.new_topic.files;
            $scope.new_topic.$save(function(topic){
                angular.forEach(topic_files, function(topic_file) {
                    topic_file.topic = topic.id;
                    delete topic_file.file;
                    topic_file.$patch().then(function(comment_file_complete) {
                        topic.files.push(comment_file_complete);
                    });
                });
                $state.go('classroom.topicDetail', {topicId: topic.id});
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
            $scope.forums.filter(function(t) {
                if (t.id == $scope.new_topic.forum)
                    $scope.forum_category = t.category
                    $scope.groups_ids = t.groups_ids
                }
            );
            $scope.list_categories = $scope.forum_category;
            if ($scope.forum_category.length > 0)
                $scope.category_id = $scope.forum_category[0].id;

            let filteredGroups = $scope.groups_ids.filter(value =>  $scope.user.groups_ids.includes(value));

            if(filteredGroups.length > 0) {
                $scope.pinned = true;
            } else {
                $scope.pinned = false;
            } 
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
})();