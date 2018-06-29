(function(angular){
    'use strict';
    var app = angular.module('discussion.filters', []);

    app.filter('actionFilter',function(){
        return function(txt) { // [ação no] tópico tal
            var filtered;
            switch(txt) {
                case 'new_comment':
                    filtered = 'comentou no';
                    break;
                case 'new_topic':
                    filtered = 'criou o';
                    break;
                case 'new_reaction':
                    filtered = 'gostou do';
                    break;
                case 'new_reaction_comment':
                    filtered = 'gostou de um comentário no';
                    break;
            }
            return filtered;
        }
    });

    app.filter('dateFilter',function(){
        return function(dt) {
            if (dt === undefined){
              return;
            }
            var past = new Date(dt),
                now = new Date(),
                diff = now.getTime() - past.getTime(),
                labels = {
                    //'ano': 31536000000,
                    'mês': 2592000000,
                    //'semana': 604800000,
                    'dia': 86400000,
                    'hora': 3600000,
                    'minuto': 60000,
                    'segundo': 1000
                },
                time_int,
                filtered = [];
            angular.forEach(labels,function(val,time_unit){
                time_int = Math.floor(diff/val);
                if(diff>=val && time_int > 0) {
                    if(time_int > 1 && time_unit != "mês") {
                        time_unit = time_unit+'s';
                    }
                    filtered.push({
                        'time_int':time_int,
                        'time_unit':time_unit
                    });
                }
            });
            if(filtered[0] === undefined) return ""; // prevent runtime error with undefined
            if(filtered[0].time_unit == "mês" && filtered[0].time_int > 1) {
                return "em "+past.getDate()+"/"+(past.getMonth()+1)+"/"+past.getFullYear()+", às "+past.getHours()+":"+past.getMinutes();
            }
            else {
                return "há "+filtered[0].time_int+" "+filtered[0].time_unit;
            }
        }
    });

    app.filter('charLimiter', ['$filter', function($filter) {
        return function(input, max_length) {
            if(input.length <= max_length){
                // If the input is smaller than the length provided, do nothing
                return input;
            } else {
                // Otherwise, limit the length of the content and add "..."
                return $filter('limitTo')(input, max_length) + "...";
            }
        };
    }]);

})(window.angular);
