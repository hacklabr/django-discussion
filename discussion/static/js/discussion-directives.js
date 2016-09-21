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
                    // isTopic: '=',
                },
                // controller: ['$scope', 'TopicFile', 'CommentFile', function($scope, TopicFile, CommentFile){
                //     // $scope.deleteFile = function(i, post_files){
                //     //     if($scope.isTopic)
                //     //         TopicFile.delete({id: post_files[i].id});
                //     //     else
                //     //         CommentFile.delete({id: post_files[i].id});
                //     //     post_files.splice(i,1);
                //     // };
                // }],
            };
        }
    );

})(window.angular);
