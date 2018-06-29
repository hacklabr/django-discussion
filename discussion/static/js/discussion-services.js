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

    app.factory('TopicPage', ['$resource', function($resource){
        return $resource('/discussion/api/topic_page');
    }]);

    app.factory('TopicLike', ['$resource', function($resource){
        return $resource('/discussion/api/topic_like/:id',
            {'id' : '@id'},
            {'update': {'method': 'PUT'} });
    }]);

    app.factory('TopicRead', ['$resource', function($resource){
        return $resource('/discussion/api/topic-read/:id',
            {'id' : '@id'},
            {'save': {'method': 'POST', 'ignoreLoadingBar': true} });
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

    app.factory('ContentFile', ['$resource', 'Upload', function($resource, Upload){
      var content_file = $resource('/discussion/api/content-file/:id',
          {'id' : '@id'},
          {
              'update': {'method': 'PUT'},
              'patch': {'method': 'PATCH'}
          });

        content_file.upload = function (blobInfo, success, failure) {
            if(blobInfo === undefined) return;

            Upload.upload(
                {
                    url: '/discussion/api/content-file',
                    data: {
                        name: blobInfo.filename(),
                        file: blobInfo.blob()
                    },
                    arrayKey: '',
                }
            ).then(function (response) {
                success(response.data.file);
            }, function (response) {
                if (response.status > 0) {
                    success('');  // disable the temporary image in the editor to let the user know about the error
                }
            });
        };
        return content_file;
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
