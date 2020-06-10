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
                    isForum: '='
                },
                controller: ['$scope', 'ForumFile', 'TopicFile', 'CommentFile', function($scope, ForumFile, TopicFile, CommentFile){
                    $scope.deleteFile = function(i){
                        if($scope.isTopic)
                            TopicFile.delete({id: $scope.files[i].id});
                        else if ($scope.isForum)
                            ForumFile.delete({id: $scope.files[i].id});
                        else
                            CommentFile.delete({id: $scope.files[i].id});
                        $scope.files.splice(i,1);
                    };
                }],
            };
        }
    );

    app.directive('hasGroupPermission',
        function() {
            return {
                restrict: "A",
                scope: {
                    hasGroupPermission: '='
                },
                link: function(scope, element, attrs) {
                    element.hide();
                    if (['professors', 'Avante'].some(function (g){
                        return scope.hasGroupPermission.indexOf(g) >= 0
                    })) {
                        element.show();
                    }
                }
            }
        }
    );

})(window.angular);
