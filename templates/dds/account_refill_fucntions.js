    function SelectAccountFromCheck(el) {
        $el = $(el);
        var this_id = $el.data('id');
        var $tbody = $el.parents('tbody');
        $('tr', $tbody).each(function (index, element) {
            var $tr = $(element);
            if ($('input[type=checkbox]', $tr).data('id') != this_id) {
                $tr.removeClass('green_bg');
                $('input[type=checkbox]', $tr).attr('checked', false);
            }
        });
        if ($el.is( ":checked" )) {
            $el.parents('tr').addClass('green_bg');
            $account_input = $('input[name="account"]').val($el.val());
        } else {
            $el.parents('tr').removeClass('green_bg');
            $account_input = $('input[name="account"]').val("");
        }
    }
    function load_account_detaild(param_name, param_value) {
        data = {};
        data[param_name] = param_value;
        /* получаем данные из схемы */
        $.ajax({
                tape: 'POST',
                url: '/dds/api/dds_accounts_rest/',
                dataType: "json",
                data: data
            })
            .done(function (result) {
                var $error_block = $('#nodata_error');
                var $datatable = $('table#account_datatable');
                var $datatable_body = $('tbody', $datatable);
                var $js_template = $('#tmpl_account_table').html();
                /* шаблон таблицы */

                /* очищаяем таблицу, если она заполнена */
                $datatable_body.empty();

                /* Стандартная постобработка */
                if (result.results && result.results.length > 0) {                              /* Если из схемы получены строки ( data json['data'] не пуста )*/
                    for (var i = 0, data_len = result.results.length; i < data_len; i++) {   /* проходим по массиву данных из схемы result.data */
                        var el = result.results[i];
                        var tr = Mustache.to_html($js_template, el);
                        /* создаем шаблонный объект с данными из элемента массива */
                        $datatable_body.append(tr);
                        /* вставляем щаблонный объект (строчку) в таблицу */
                        $datatable.removeClass('none');
                        $error_block.addClass('none');
                    }
                } else {
                    $error_block.removeClass('none');
                    return false;
                }
            });
    }