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

})(window.angular);
