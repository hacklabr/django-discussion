(function(angular){
    'use strict';
    var app = angular.module('discussion.services', ['ngResource']);

    app.factory('Forum', ['$resource', function($resource){
        return $resource('/discussion/api/forum/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('Topic', ['$resource', function($resource){
        return $resource('/discussion/api/topic/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('TopicLike', ['$resource', function($resource){
        return $resource('/discussion/api/topic_like/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('Comment', ['$resource', function($resource){
        return $resource('/discussion/api/comment/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('CommentLike', ['$resource', function($resource){
        return $resource('/discussion/api/comment_like/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('Notification', ['$resource', function($resource){
        return $resource('/discussion/api/topic-notification/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('TopicFile', ['$resource', 'Upload', function($resource, Upload){
         var topic_file = $resource('/discussion/api/topic-file/:id',
            {'id' : '@id'},
            {
                'update': {'method': 'PUT'},
                'patch': {'method': 'PATCH'}
            });

        topic_file.upload = function(file) {
            return Upload.upload({
                url: '/discussion/api/topic-file',
                data: {
                    name: file.name,
                    file: file
                },
                arrayKey: '',
            });
        };
        return topic_file;
    }]);

    app.factory('CommentFile', ['$resource', 'Upload', function($resource, Upload){
        var comment_file = $resource('/discussion/api/comment-file/:id',
            {'id' : '@id'},
            {
                'update': {'method': 'PUT'},
                'patch': {'method': 'PATCH'}
            });

        comment_file.upload = function(file) {
            return Upload.upload({
                url: '/discussion/api/comment-file',
                data: {
                    name: file.name,
                    file: file
                },
                arrayKey: '',
            });
        };
        return comment_file
    }]);

    app.factory('Category', ['$resource', function($resource){
        return $resource('/discussion/api/category/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('Tag', ['$resource', function($resource){
        return $resource('/discussion/api/tag/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

})(window.angular);
