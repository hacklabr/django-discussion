(function(angular){
    'use strict';

    var app = angular.module('discussion', [
        'discussion.controllers',
        'discussion.services',
        'ui.tinymce',
    ]);

    app.config(['$resourceProvider', function($resourceProvider) {
          // Don't strip trailing slashes from calculated URLs
          $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);
})(angular);
