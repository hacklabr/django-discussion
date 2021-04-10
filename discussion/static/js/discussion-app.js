(function(angular){
    'use strict';

    var app = angular.module('discussion', [
        'gettext',
        'discussion.controllers',
        'discussion.services',
        'discussion.directives',
        'discussion.filters',
        'core.services',
        'ngRoute',
        'ui.tinymce',
        'ui.bootstrap',
        'ngFileUpload',
        'ui.select',
        'ngSanitize',
        'ngAnimate',
        'duScroll',
        'LocalStorageModule',
        'shared',
        'djangular'
    ]);

    // Set new default values for 'duScroll'
    app.value('duScrollDuration', 1000);
    app.value('duScrollOffset', 100);

    angular.module('discussion').run(['gettextCatalog', 'UserLocalStorage', function (gettextCatalog, UserLocalStorage) {
        let defaultLanguage = UserLocalStorage.get('currentLanguage') || 'en';

        gettextCatalog.setCurrentLanguage(defaultLanguage);
        UserLocalStorage.set('currentLanguage', defaultLanguage);

        //UserLocalStorage.set('currentLanguage', 'en');
        gettextCatalog.setStrings('es', {"By":"Por","Courses":"Cursos","Date":"Fecha","Forums":"Foros","From":"De","Here you find a resumy of the most important things of the academy. Enjoy and have a fun learning ;D":"Aquí encontrará un resumen de las cosas más importantes de la academia. Disfruta y diviértete aprendiendo ;D","Last activity":"Última actividad","Learn how to use":"Aprender cómo usar","Notifications":"Notificaciones","See all notifications":"Ver todas las notificaciones","This forum doesn't have any topics yet.":"Este foro aún no tiene ningún tema.","View all forums":"Ver todos los foros","Welcome to the Academy!":"¡Bienvenidos a la Academia!","You have":"Tú tienes","categories":"categorias","hide":"esconder","latest posts":"últimas publicaciones","learn more practices":"aprender más prácticas","published by":"publicado por","reactions":"reacciones","see":"ver","tags":"tags","topic":"tema","unread notification":"notificación no leída","unread notifications":"notificaciones no leídas", "Dashboard":"Panel","commented on the topic":"comentó sobre el tema","in the forum":"en el foro","ago":"atrás","comment":"comentario","liked":"gusta", "Courses":"Cursos","Loading courses...":"Cargando cursos...","START DATE":"FECHA DE INICIO","There are no courses.":"No hay cursos.","WHAT YOU LEARN AT THIS COURSE":"LO QUE APRENDES EN ESTE CURSO", "Administration":"Administración","Administração":"Administração","Back to the plataform":"De vuelta al plataform","Cancel":"Cancelar","Clean":"Limpiar","Contact":"Contacto","Courses":"Cursos","Hi":"Olá","Login":"Acceso","Logout":"Cerrar sesión","Profile":"Perfil","Register":"Registrarse","Send":"Enviar","Suport":"Apoyo","Latest topics":"Últimos temas","Load more":"Carga más","Create new topic":"Crear nuevo tema","Assign TAGs to the topic":"Asignar TAGs al tema","Attach file":"Adjuntar archivo","Choose a category":"Elige una categoría","Choose the forum":"Elige el foro","Forum is required field":"El foro es un campo obligatorio","Post new topic":"Nuevo tema","Required fields":"Campos requeridos","Topic cannot be empty":"El tema no puede estar vacío","Topic text":"Texto del tema","Topic title is required field":"El título del tema es un campo obligatorio","What is the category of your topic?":"¿Cuál es la categoría de su tema?","What is the title of the new topic?":"¿Cuál es el título del nuevo tema?","Which forum should the new topic be in?":"¿En qué foro debería estar el nuevo tema?","New Topic":"Nuevo tema","Edit topic":"Editar tema","by":"por","Like":"Gusta","Comment":"Comentario","Edit":"Editar","Comments":"Comentarios", "last edition":"última edición","discard":"descarte","attach":"adjuntar"});
        gettextCatalog.setStrings('pt_br', {"By":"Por","Courses":"Cursos","Date":"Data","Forums":"Fóruns","From":"De","Here you find a resumy of the most important things of the academy. Enjoy and have a fun learning ;D":"Aqui você encontra um resumo das coisas mais importantes da academia. Aproveite e divirta-se aprendendo ;D","Last activity":"Última atividade","Learn how to use":"Aprenda a usar","Notifications":"Avisos","See all notifications":"Ver todos os avisos","This forum doesn't have any topics yet.":"Este fórum ainda não tem nenhum tópico.","View all forums":"Ver todos os fóruns","Welcome to the Academy!":"Bem-vindo à Academia!","You have":"Você tem","categories":"categorias","hide":"ocultar","latest posts":"últimas postagens","learn more practices":"aprender mais práticas","published by":"publicado por","reactions":"reações","see":"ver","tags":"tags","topic":"tópico", "Dashboard": "Painel","commented on the topic":"comentou no tópico","in the forum":"no fórum","ago":"atrás","comment":"comentário","liked":"gostou", "Courses":"Cursos","Loading courses...":"Carregando cursos...","START DATE":"DATA DE INÍCIO","There are no courses.":"Não há cursos.","WHAT YOU LEARN AT THIS COURSE":"O QUE VOCÊ APRENDE NESTE CURSO", "Administration":"Administração","Back to the plataform":"Voltar para a plataforma","Cancel":"Cancelar","Clean":"Limpar","Contact":"Contato","Courses":"Cursos","Hi":"Olá","Login":"Acessar","Logout":"Sair","Profile":"Perfil","Register":"Registrar","Send":"Enviar","Suport":"Suporte","Latest topics":"Últimos tópicos","Load more":"Carregar mais","Create new topic":"Criar novo tópico","Assign TAGs to the topic":"Atribuir TAGs ao tópico","Attach file":"Anexar arquivo","Choose a category":"Escolha uma categoria","Choose the forum":"Escolha o fórum","Forum is required field":"O fórum é um campo obrigatório","New Topic":"Novo topico","Post new topic":"Postar novo tópico","Required fields":"Campos obrigatórios","Topic cannot be empty":"O tópico não pode estar vazio","Topic text":"Texto do tópico","Topic title is required field":"O título do tópico é um campo obrigatório","What is the category of your topic?":"Qual é a categoria do seu tópico?","What is the title of the new topic?":"Qual é o título do novo tópico?","Which forum should the new topic be in?":"Em qual fórum o novo tópico deve estar?","Edit topic":"Editar tópico","by":"por","Like":"Gostar","Comment":"Comentar","Edit":"Editar","Comments":"Comentários","last edition":"última edição","discard":"descartar","attach":"anexar"});
    }]);

    app.config(['$locationProvider', '$routeProvider', 'localStorageServiceProvider',
        function config($locationProvider, $routeProvider,
            localStorageServiceProvider) {
            localStorageServiceProvider.setPrefix('');
            $locationProvider.hashPrefix('!');

            $routeProvider.
                when('/topic/new/', {
                    templateUrl: 'topic-new.html',
                    controller: 'NewTopicCtrl'
                }).
                when('/topic/:topicId/', {
                    templateUrl: 'topic-detail.html',
                    controller: 'TopicCtrl'
                }).
                when('/forum/embed/', {
                    templateUrl: 'forum-embed.html',
                    controller: 'ForumEmbedCtrl',
                    reloadOnSearch: false
                }).
                when('/forum/:forumId', {
                    templateUrl: 'forum.html',
                    controller: 'ForumCtrl',
                    reloadOnSearch: false
                }).
                when('/', {
                    templateUrl: 'forum.html',
                    controller: 'ForumCtrl',
                    reloadOnSearch: false
                }).
                otherwise('/');
        }
    ]);
})(angular);
