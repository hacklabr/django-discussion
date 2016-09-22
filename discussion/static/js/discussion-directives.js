(function(angular) {
    'use strict';
    var app = angular.module('discussion.directives', []);

    app.directive('files',
        function() {
            return {
                restrict: "E",
                templateUrl: "/static/templates/files.html",
                scope: {
                    files: '=',
                    progress: '=',
                    editable: '=',
                    isTopic: '=',
                },
                controller: ['$scope', 'TopicFile', 'CommentFile', function($scope, TopicFile, CommentFile){
                    $scope.deleteFile = function(i){
                        if($scope.isTopic)
                            TopicFile.delete({id: $scope.files[i].id});
                        else
                            CommentFile.delete({id: $scope.files[i].id});
                        $scope.files.splice(i,1);
                    };
                }],
            };
        }
    );

})(window.angular);
