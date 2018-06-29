(function(angular){
    'use strict';

    var app = angular.module('ui.tinymce');

    // If you want to cutomize uiTinymceConfig for your theme, please copy this file to you theme in the
    // same path (static/js/). This are the default setting for timtec
    app.value('uiTinymceConfig', {
        base_url: '/static/tinymce-dist/',
        related_url: true,
        inline: false,
        menubar: false,
        relative_urls: false,
        remove_script_host: false,
        plugins : 'advlist lists autolink link image media autoresize',
        toolbar: 'bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | quicklink link image media fullscreen | removeformat',
        skin: 'lightgray',
        theme : 'modern',
        language: 'pt_BR',
        language_url : '/static/vendor/tinymce/langs/pt_BR.js',
        resize: true,
        elementpath: false,

        format: {
          removeformat: [
            {selector: 'font', remove : 'all', split : true, expand : false, block_expand: true, deep : true},
            {selector: 'span', attributes : ['style', 'class'], remove : 'all', split : true, expand : false, deep : true},
            {selector: '*', attributes : ['style', 'class'], split : false, expand : false, deep : true}
          ]
        },

        // media customizations
        media_poster: false,
        media_alt_source: false,
        media_dimensions: false,
        media_url_resolver: function (data, resolve/*, reject*/) {
            var complete_url = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var result = complete_url.exec(data.url);
            if (result && result[2].length == 11) {
                var youtube_id = result[2];
                var embedHtml = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+ youtube_id +'" frameborder="0" allowfullscreen></iframe>';
                resolve({html: embedHtml});
            } else {
                resolve({html: ''});
            }
        },

        // Removing loading spinner
        setup: function (editor) {
            $('.tinymce-loading').hide();
        },

        // Image upload
        // enable title field in the Image dialog
        image_title: false,
        image_description: false,
        image_dimensions: false,
        // enable automatic uploads of images represented by blob or data URIs
        automatic_uploads: true,
        // here we add custom filepicker only to Image dialog
        file_picker_types: 'image',
        // and here's our custom image picker
        file_picker_callback: function(cb, value, meta) {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');
            input.style.display = 'none';

            // Note: In modern browsers input[type="file"] is functional without
            // even adding it to the DOM, but that might not be the case in some older
            // or quirky browsers like IE, so you might want to add it to the DOM
            // just in case, and visually hide it. And do not forget do remove it
            // once you do not need it anymore.
            document.body.appendChild(input);

            input.onchange = function() {
                var file = this.files[0];

                // Note: Now we need to register the blob in TinyMCEs image blob
                // registry. In the next release this part hopefully won't be
                // necessary, as we are looking to handle it internally.
                var id = 'blobid' + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var blobInfo = blobCache.create(id, file);
                blobCache.add(blobInfo);

                // call the callback and populate the Title field with the file name
                cb(blobInfo.blobUri(), { title: file.name });
            };

            input.click();
          }
    });

})(window.angular);
