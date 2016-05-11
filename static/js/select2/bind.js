(function($){				
	jQuery.fn.bindselect2 = function(){
            var $el = this;
            var url = $el.attr('data-url');
            var field = $el.attr('data-field');
            var placeholder = $el.attr('data-placeholder');
            var minlength = $el.attr('data-minlength');
            var filter_field = $el.attr('data-filter_field');


            $el.select2({
                        "language": "ru",
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
                                            text: item.name,
                                            id: item.pk
                                        }})};}},
                        minimumInputLength: minlength,
                        escapeMarkup: function (markup) {
                            return markup;
                        }
                });
	};	
})(jQuery);