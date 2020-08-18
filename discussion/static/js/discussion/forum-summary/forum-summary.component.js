(function() {
    'use strict';
    angular.
        module('forumSummary').
        component('forumSummary', {
            templateUrl: '/discussion/forum-summary.template.html',
            controller: ForumCtrl,
            bindings: {
                forum: '<',
            },
        });

    ForumCtrl.$inject = [
        '$scope',
        '$routeParams',
        '$stateParams',
        '$http',
        '$location',
        'Category',
        'Forum',
        'ForumPage',
        'Tag',
        'Topic',
        'TopicPage',
        'CurrentUser'
    ];

    function ForumCtrl ($scope, $routeParams, $stateParams, $http, $location, Category, Forum, ForumPage, Tag, Topic, TopicPage, CurrentUser) {

        var ctrl = this;
        const forum_id = $stateParams.forumId;

        $scope.user = CurrentUser;
        if(ctrl.forum)
            $scope.forum = ctrl.forum
        else
            $scope.forum = {}

        $scope.topics = {}
        $scope.search = {txt:""}
        // Pagination Params
        $scope.forum_pages_max_number = 20;
        ctrl.forum_topics_page = 20;
        $scope.forum.current_page = 1
        
        if(forum_id) {
            singleInit();
        } else {
            console.error("no forum id provided")
        }

        function singleInit() {
            Forum.get({id: forum_id}, (forum) => {
                $scope.filters = undefined;
                $scope.forum_search = false;
                $scope.forum_single = true;
                $scope.forums = [];
                $scope.topics.current_page = 1;
                $scope.forum.page = TopicPage.get({
                    page: 1,
                    page_size: ctrl.forum_topics_page,
                    forum: forum_id,
                    ordering: '-last_activity_at'},
                    function(page){
                        $scope.forum.topics = page.results;
                        $scope.topics_loaded = true;
                        ctrl.forum.topics_total = page.count;
                        ctrl.forum.topics = $scope.forum.topics
                    },
                    function(err){
                        console.log("Erro ao carregar os tópicos", err);
                    }
                );
                $scope.forums.push(forum); // to reuse template's ng-repeat
            },function(err){
                console.error(err)
            });
        }


        // Pagination controls
        $scope.topicPageChanged = function(){
          $scope.forum.page = TopicPage.get({
              page: ctrl.topics.current_page,
              page_size: ctrl.forum_topics_page,
              forum: forum_id,
              ordering: '-last_activity_at'},
              function(page){
                  $scope.forum.topics = page.results;
                  $scope.topics_loaded = true;
                  ctrl.forum.topics = $scope.forum.topics
              },
              function(err){
                  console.log("Erro ao carregar os tópicos");
              }
          );
        };

        $scope.getResults = function(txt) {
            $scope.current_search = txt;
            TopicPage.get({
                search: txt,
                page: 1,
                page_size: ctrl.forum_topics_page,
                ordering: '-last_activity_at',
                ignoreLoadingBar: true},
                function(page){
                    $scope.forum.title = "Resultados de busca";
                    $scope.topics.current_page = 1;
                    $scope.forum.topics = page.results;
                    $scope.topics_loaded = true;
                    
                    $scope.filters = undefined;
                    $scope.forum_search = true;
                    $scope.forum_single = false;
                    $scope.forums.push($scope.forum); // to reuse template's ng-repeat
                    ctrl.forum.topics_total = page.count;
                    ctrl.forum.topics = $scope.forum.topics
                }, function(err){
                    console.error(err)
                });
        }
    }
})();