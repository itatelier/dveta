    function SelectAccountFromCheck(el) {
        $el = $(el);
        var this_id = $el.data('id');
        var $tbody = $el.parents('tbody');
        var $value_input = $('input[name="'+ $tbody.attr('rel') + '"');
        $('tr', $tbody).each(function (index, element) {
            var $tr = $(element);
            if ($('input[type=checkbox]', $tr).data('id') != this_id) {
                $tr.removeClass('green_bg');
                $('input[type=checkbox]', $tr).attr('checked', false);
            }
        });
        if ($el.is( ":checked" )) {
            $el.parents('tr').addClass('green_bg');
            $value_input.val($el.val());
        } else {
            $el.parents('tr').removeClass('green_bg');
            $value_input.val("");
        }
    }
    function load_account_detail(table_rel, field, param_value) {
        data = {};
        data[field] = param_value;
        /* получаем данные из схемы */
        $.ajax({
                tape: 'POST',
                url: '/dds/api/dds_accounts_rest/',
                dataType: "json",
                data: data
            })
            .done(function (result) {
                var $error_block = $('#nodata_error');
                var $datatable = $('table[rel="'+table_rel+'"]');
                var $datatable_body = $('tbody', $datatable);
                var $js_template = $('#tmpl_account_table').html();

                /* очищаяем таблицу, если она заполнена */
                $datatable_body.empty();

                /* Стандартная постобработка */
                if (result.results && result.results.length > 0) {                              /* Если из схемы получены строки ( data json['data'] не пуста )*/
                    for (var i = 0, data_len = result.results.length; i < data_len; i++) {   /* проходим по массиву данных из схемы result.data */
                        if (data_len == 1 && result.results[i].status) {
                            result.results[i].checked = 1;
                            var input_name = $('tbody', $datatable).attr('rel');
                            console.log("---Status: " + result.results[i].status);
                            $('input[name="' + input_name + '"]').val(result.results[i].pk);
                        }
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

    function load_items_by_group(target_select_rel, selected_group_id, selected_item) {
        var $item_select = $('select#'+target_select_rel);
        $.ajax({
            tape: 'POST',
            url: '/dds/api/dds_items_rest/',
            dataType: "json",
            data: { "item_group": selected_group_id}
        })
        .done(function (result) {
            $item_select.empty();

            for (var i = 0, data_len = result.results.length; i < data_len; i++) {
                var selected = "";
                if (result.results[i].pk == selected_item) {
                    selected = "SELECTED"
                }
                var option = "<option value=\"" + result.results[i].pk + "\" "+selected+">" + result.results[i].name + "</option>";
                $item_select.append(option);
            }
        });
    }