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

    angular.module('discussion').run(['gettextCatalog', function (gettextCatalog) {

        gettextCatalog.setStrings('es', {"By":"Por","Courses":"Cursos","Date":"Fecha","Forums":"Foros","From":"De","Here you find a resumy of the most important things of the academy. Enjoy and have a fun learning ;D":"Aquí encontrará un resumen de las cosas más importantes de la academia. Disfruta y diviértete aprendiendo ;D","Last activity":"Última actividad","Learn how to use":"Aprender cómo usar","Announcements":"Avisos","See all announcements":"Ver todas las notificaciones","This forum doesn't have any topics yet.":"Este foro aún no tiene ningún tema.","View all forums":"Ver todos los foros","Welcome to the Academy!":"¡Bienvenidos a la Academia!","You have":"Tú tienes","categories":"categorias","hide":"esconder","Latest posts":"Últimas publicaciones","learn more practices":"aprender más prácticas","published by":"publicado por","reactions":"reacciones","see":"ver","tags":"tags","topic":"tema","unread announcement":"notificación no leída","unread announcements":"notificaciones no leídas", "Dashboard":"Panel","commented on the topic":"comentó sobre el tema","in the forum":"en el foro","ago":"atrás","comment":"comentario","liked":"gustos", "Courses":"Cursos","Loading courses...":"Cargando cursos...","START DATE":"FECHA DE INICIO","There are no courses.":"No hay cursos.","WHAT YOU LEARN AT THIS COURSE":"LO QUE APRENDES EN ESTE CURSO", "Administration":"Administración","Administração":"Administração","Back to the plataform":"De vuelta al plataform","Cancel":"Cancelar","Clean":"Limpiar","Contact":"Contacto","Courses":"Cursos","Hi":"Olá","Login":"Acceso","Logout":"Cerrar sesión","Profile":"Perfil","Register":"Registrarse","Send":"Enviar","Suport":"Apoyo","Latest topics":"Últimos temas","Load more":"Carga más","Create new topic":"Crear nuevo tema","Assign TAGs to the topic":"Asignar TAGs al tema","Attach file":"Adjuntar archivo","Choose a category":"Elige una categoría","Choose the forum":"Elige el foro","Forum is required field":"El foro es un campo obligatorio","Post new topic":"Nuevo tema","Required fields":"Campos requeridos","Topic cannot be empty":"El tema no puede estar vacío","Topic text":"Texto del tema","Topic title is required field":"El título del tema es un campo obligatorio","What is the category of your topic?":"¿Cuál es la categoría de su tema?","What is the title of the new topic?":"¿Cuál es el título del nuevo tema?","Which forum should the new topic be in?":"¿En qué foro debería estar el nuevo tema?","New Topic":"Nuevo tema","Edit topic":"Editar tema","by":"por","Like":"Gusta","Comment":"Comentario","Edit":"Editar","Comments":"Comentarios", "last edition":"última edición","discard":"descarte","attach":"adjuntar","comments":"comentarios","Latest Posts":"Últimas publicaciones","View all topics in this forum":"Ver todos los temas de este foro","No results found":"No se han encontrado resultados","A place for people chat and interact.":"Un lugar para que la gente charle e interactúe.","CATEGORY": "CATEGORÍA","Select...": "Seleccione...","Clear filters": "Eliminar filtros","Topics": "Temas","Back":"Volver","Filter result":"Filtrar resultados","Displaying":"Visualización","of":"de","topics": "temas",
        "topic":"tema","in forum":"en el foro","replied to":"responder a","an activity":"una actividad","in":"en el","commented on":"comentado","created the":"creó el","liked the":"me gustó el","did you like a comment on":"te gustó un comentario sobre"});
        gettextCatalog.setStrings('pt_br', {"By":"Por","Courses":"Cursos","Date":"Data","Forums":"Fóruns","From":"De","Here you find a resumy of the most important things of the academy. Enjoy and have a fun learning ;D":"Aqui você encontra um resumo das coisas mais importantes da academia. Aproveite e divirta-se aprendendo ;D","Last activity":"Última atividade","Learn how to use":"Aprenda a usar","Announcements":"Avisos","See all announcements":"Ver todos os avisos","This forum doesn't have any topics yet.":"Este fórum ainda não tem nenhum tópico.","View all forums":"Ver todos os fóruns","Welcome to the Academy!":"Bem-vindo à Academia!","You have":"Você tem","categories":"categorias","hide":"ocultar","Latest posts":"Últimas postagens","learn more practices":"aprender mais práticas","published by":"publicado por","reactions":"reações","see":"ver","tags":"tags","topic":"tópico", "Dashboard": "Painel","commented on the topic":"comentou no tópico","in the forum":"no fórum","ago":"atrás","comment":"comentário","liked":"gostaram", "Courses":"Cursos","Loading courses...":"Carregando cursos...","START DATE":"DATA DE INÍCIO","There are no courses.":"Não há cursos.","WHAT YOU LEARN AT THIS COURSE":"O QUE VOCÊ APRENDE NESTE CURSO", "Administration":"Administração","Back to the plataform":"Voltar para a plataforma","Cancel":"Cancelar","Clean":"Limpar","Contact":"Contato","Courses":"Cursos","Hi":"Olá","Login":"Acessar","Logout":"Sair","Profile":"Perfil","Register":"Registrar","Send":"Enviar","Suport":"Suporte","Latest topics":"Últimos tópicos","Load more":"Carregar mais","Create new topic":"Criar novo tópico","Assign TAGs to the topic":"Atribuir TAGs ao tópico","Attach file":"Anexar arquivo","Choose a category":"Escolha uma categoria","Choose the forum":"Escolha o fórum","Forum is required field":"O fórum é um campo obrigatório","New Topic":"Novo topico","Post new topic":"Postar novo tópico","Required fields":"Campos obrigatórios","Topic cannot be empty":"O tópico não pode estar vazio","Topic text":"Texto do tópico","Topic title is required field":"O título do tópico é um campo obrigatório","What is the category of your topic?":"Qual é a categoria do seu tópico?","What is the title of the new topic?":"Qual é o título do novo tópico?","Which forum should the new topic be in?":"Em qual fórum o novo tópico deve estar?","Edit topic":"Editar tópico","by":"por","Like":"Gostar","Comment":"Comentar","Edit":"Editar","Comments":"Comentários","last edition":"última edição","discard":"descartar","attach":"anexar","unread announcement":"aviso não lido","unread announcements":"avisos não lidos","comments":"comentários","Latest Posts":"Últimas postagens","View all topics in this forum":"Ver todos os tópicos deste fórum","No results found":"Nenhum resultado encontrado","A place for people chat and interact.":"Um lugar para as pessoas conversarem e interagirem.","CATEGORY": "CATEGORIA","Select...": "Selecionar...","Clear filters": "Limpar filtros","Topics": "Tópicos","Back":"Voltar","Filter result":"Filtrar resultados","Displaying":"Exibindo","of":"de","topics": "tópicos",
        "topic":"tópico","in forum":"no fórum","replied to":"respondeu a","an activity":"uma atividade","in":"no","commented on":"comentou no","created the":"criou o","liked the":"gostou do","did you like a comment on":"gostou de um comentário no"});
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
