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

//    app.factory('', ['$resource', function($resource){
//        return $resource('/api//:id',
//            {'id' : '@id'},
//            {'update': {'method': 'PUT'} });
//    }]);

})(window.angular);
