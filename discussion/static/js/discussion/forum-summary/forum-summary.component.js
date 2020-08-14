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

        // var ctrl = this;
        const forum_id = $stateParams.forumId;

        $scope.user = CurrentUser;
        $scope.forum = {}
        $scope.topics = {}
        $scope.search = {txt:""}
        // Pagination Params
        $scope.forum_pages_max_number = 20;
        $scope.forum_topics_page = 20;
        $scope.forum.page_size = 20;
        $scope.forum.current_page = 1

        if(forum_id) {
            singleInit();
        } else {
            normalInit();
        }

        function singleInit() {
            Forum.get({id: forum_id}, (forum) => {
                $scope.filters = undefined;
                $scope.forum_search = false;
                $scope.forum_single = true;
                $scope.forums = [];
                $scope.forum = forum;
                $scope.topics.current_page = 1;
                $scope.forum.page = TopicPage.get({
                    page: 1,
                    page_size: $scope.forum_topics_page,
                    forum: forum_id,
                    ordering: '-last_activity_at'},
                    function(page){
                        $scope.forum.topics = page.results;
                        $scope.forum_topics_total = page.count;
                        $scope.topics_loaded = true;
                    },
                    function(err){
                        console.log("Erro ao carregar os tópicos");
                    }
                );
                $scope.forums.push(forum); // to reuse template's ng-repeat
            },function(err){
                normalInit();
            });
        }

        function normalInit() {
            $scope.filters = {};
            $scope.forum_single = false;
            const categoriesParams = $routeParams['categories'];
            const tagParams = $routeParams['tags']

            if(categoriesParams || tagParams) {
                if(categoriesParams) {
                    if(typeof categoriesParams === 'string' || typeof categoriesParams === 'number')
                        $scope.filters.categories = [categoriesParams];
                    else
                        $scope.filters.categories = categoriesParams;

                    $scope.filters.categories = $scope.filters.categories.map(function(cat) {
                        return angular.fromJson(cat);
                    });
                }
                else {
                    $scope.filters.categories = [];
                }
                if(tagParams) {
                    if(typeof tagParams === 'string' || typeof tagParams === 'number')
                        $scope.filters.tags = [tagParams];
                    else
                        $scope.filters.tags = tagParams;
                    $scope.filters.tags = $scope.filters.tags.map(function(tag) {
                        return angular.fromJson(tag);
                    });
                }
                else {
                    $scope.filters.tags = [];
                }
                $scope.forum_search = true;
            }
            else {
                $scope.filters.categories = [];
                $scope.filters.tags = [];
                $scope.forum_search = false;
            }

            $scope.forums = ForumPage.get({
                search: $scope.current_search,  // if there is a search in progress, keep it
                page: $scope.forum.current_page,
                page_size: $scope.forum.page_size,
            }, (response) => {
                $scope.forums = response.results
                $scope.forum.total_forum_items = response.count
                $scope.forum.max_size = response.length
                $scope.forum_page_loaded = response.$resolved;
                $scope.forum.has_next_page = (response.next !== null || response.previous !== null)
            });
            $scope.latest_topics = Topic.query({
                limit: 6,
                ordering: '-last_activity_at',
                }, function(){
                    $scope.topics_loaded = true;
                }
            );
        }


        // Pagination controls
        $scope.topicPageChanged = function(){
          $scope.forum.page = TopicPage.get({
              search: $scope.current_search,  // if there is a search in progress, keep it
              page: $scope.topics.current_page,
              page_size: $scope.forum_topics_page,
              forum: forum_id,
              ordering: '-last_activity_at'},
              function(page){
                  $scope.forum.topics = page.results;
                  $scope.topics_loaded = true;
              },
              function(err){
                  console.log("Erro ao carregar os tópicos");
              }
          );
        };
        $scope.forumPageChanged = () => {
            $scope.forums = ForumPage.get({
                search: $scope.current_search,  // if there is a search in progress, keep it
                page: $scope.forum.current_page,
                page_size: $scope.forum.page_size
            }, (response) => {
                $scope.forums = response.results
                $scope.forum.total_forum_items = response.count
                $scope.forum.max_size = response.length
                $scope.forum_page_loaded = response.$resolved;
            });
          };

        $scope.getResults = function(txt) {
            $scope.current_search = txt;
            TopicPage.get({
                search: txt,
                page: 1,
                page_size: $scope.forum_topics_page,
                ordering: '-last_activity_at',
                ignoreLoadingBar: true},
                function(page){
                    $scope.forums = [];
                    $scope.forum.title = "Resultados de busca";
                    $scope.topics.current_page = 1;
                    $scope.forum.topics = page.results;
                    $scope.forum_topics_total = page.count;
                    $scope.topics_loaded = true;

                    $scope.filters = undefined;
                    $scope.forum_search = true;
                    $scope.forum_single = false;
                    $scope.forums.push($scope.forum); // to reuse template's ng-repeat

                }, function(err){
                    normalInit();
                });
        }

        function clear_filters() {
            $scope.filters = {};
            $scope.filters.categories = [];
            $scope.filters.tags = [];
        }

        $scope.clear_search = () => {
            $scope.forum_search = false;
            $scope.current_search = "";
            $scope.forums = {}
            $scope.topics_loaded = false;
            $scope.search = {txt:""}
            normalInit()
        }

        function set_route() {
            var new_url = '#!/';
            if (forum_id)
                new_url += forum_id;
            var plain_url = true;
            for(var i = 0; i < $scope.filters.categories.length; i++) {
                if (plain_url)
                    new_url += '?categories=' + angular.toJson($scope.filters.categories[i]);
                else
                    new_url += '&categories=' + angular.toJson($scope.filters.categories[i]);
                plain_url = false;
            }
            for(var i = 0; i < $scope.filters.tags.length; i++) {
                if (plain_url)
                    new_url += '?tags=' + angular.toJson($scope.filters.tags[i]);
                else
                    new_url += '&tags=' + angular.toJson($scope.filters.tags[i]);
                plain_url = false;
            }
            window.location.hash = new_url;
        }

        $scope.forumFilter = function(operation, type, filter_obj) {

            if(!$scope.filters) {
                $scope.filters = {};
                $scope.filters.categories = []
                $scope.filters.tags = []
            }

            if(operation == 'clear') {
                clear_filters();
            }

            if(type === 'cat') {
                if(operation === 'add') {
                    $scope.filters.categories.some(obj => obj.name === filter_obj.name) ?
                        console.log('already filtering by this category') :
                        $scope.filters.categories.push(filter_obj);
                }
                else {
                    $scope.filters.categories.splice( $scope.filters.categories.indexOf(filter_obj), 1 );
                }
            }
            else {
                if(operation === 'add') {
                    $scope.filters.tags.some(obj => obj.name === filter_obj.name) ?
                        console.log('already filtering by this tag') :
                        $scope.filters.tags.push(filter_obj);
                }
                else {
                    $scope.filters.tags.splice( $scope.filters.tags.indexOf(filter_obj), 1 );
                }
            }

            if($scope.filters.categories.length + $scope.filters.tags.length === 0) {
                clear_filters();
            }

            set_route();

            $scope.forums = Forum.query({ // TODO: when single forum, filter only within it
                categories : $scope.filters.categories.map(function(el) {
                    return el.id;
                }), //array with cat id's
                tags : $scope.filters.tags.map(function(el) {
                    return el.id;
                }) //array with tag id's
            }, function(r) {
                $scope.forum_search = true;
            });
        }
    }
})();