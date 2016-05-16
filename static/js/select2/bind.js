(function($){
    jQuery.fn.select2.defaults.set("language", "ru");
	jQuery.fn.bindselect2 = function(){
            var $el = this;
            var url = $el.attr('data-url');
            var field = $el.attr('data-field');
            var placeholder = $el.attr('data-placeholder');
            var minlength = $el.attr('data-minlength');
            var filter_field = $el.attr('data-filter_field');
            var text_compose_function = $el.attr('data-text_func');
            console.log("func " + text_compose_function);

            // Функция компоновки текста. Если в файле шаблона будет прописана отдельная функция обработки, то ее наименование следует указать в параметре select'a -'data-text_func'
            function prepare_text(item) {
                if (item) {
                    var text_str;
                    if (text_compose_function) {
                        text_str = window[text_compose_function](item);
                    } else {
                        text_str = item[field];
                    }
                    return text_str;
                } else {
                    return "Field text not found! Check bind.js"
                }
            }

            $el.select2({
                        language: 'ru',
                        placeholder: placeholder,
                        allowClear: true,
                        ajax: {
                            url: url,
                            dataType: 'json',
                            delay: 250,
                            data: function (params) {
                                var return_obj = {};
                                return_obj['search'] = params.term;
                                if (filter_field) {
                                    return_obj[filter_field] = $el.attr('data-filter_value');
                                }
                                return return_obj;
                            },
                            processResults: function (data) {
                                return {
                                    results: $.map(data.results, function (item) {
                                        return {
                                            text: prepare_text(item),
                                            id: item.pk
                                        }})};}},
                        minimumInputLength: minlength,
                        escapeMarkup: function (markup) {
                            return markup;
                        }
                });
	};	
})(jQuery);