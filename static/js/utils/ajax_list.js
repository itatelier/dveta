
function listing_pager(current_page, last_page) {
    var last_offset = last_page - 3;
    var $pager_box = $('div#pager_box');
    $('a', $pager_box).remove();
    $('i', $pager_box).remove();
    if (last_page <= 7) {
        //console.log("last page <= 7");
        for (var i=1; i <= last_page;i++) {
            var current = ""; if (i == current_page) { current = "current" };
            $pager_box.append('<a href="#" class="'+current+'" onClick="SetPage('+i+')">'+i+'</a>');
        }
    } else {
        if (current_page <= 4) {
            //console.log("current <= 4");
            for (var i=1; i <=5; i++) {
                var current = ""; if (i == current_page) { current = "current" };
                $pager_box.append('<a href="#" class="'+current+'" onClick="SetPage('+i+')">'+i+'</a>');
            }
            $pager_box.append('<i>...</i>');
            $pager_box.append('<a href="#" onClick="SetPage('+last_page+')">'+last_page+'</a>');
        } else if (current_page > 4 && current_page < last_offset) {
            //console.log("current > 4");
            $pager_box.append('<a href="#" onClick="SetPage(1)">1</a>');
            $pager_box.append('<i>...</i>');
            for (var i= parseInt(current_page) -1; i <= parseInt(current_page + 1); i++) {
                var current = ""; if (i == current_page) { current = "current" };
                $pager_box.append('<a href="#" class="'+current+'" onClick="SetPage('+i+')">'+i+'</a>');
            }
            $pager_box.append('<i>...</i>');
            $pager_box.append('<a href="#" onClick="SetPage('+last_page+')">'+last_page+'</a>');
        } else if (current_page >= last_offset) {
            //console.log("current >= offset");
            $pager_box.append('<a href="#" onClick="SetPage(1)">1</a>');
            $pager_box.append('<i>...</i>');
            for (var i= parseInt(last_page) -4; i <= last_page; i++) {
                var current = ""; if (i == current_page) { current = "current" };
                $pager_box.append('<a href="#" class="'+current+'" onClick="SetPage('+i+')">'+i+'</a>');
            }
        } else {
            console.log("hm.. :/")
        }
    }
}

function SetRows(num) { /* Задаем количество строк в выводе */
    var $rows_box = $('div#rows_box');
    $('a[rel="limit"]').each(function(index,el) {
        var $a = $(el);
        if ($a.html() == num) {
            $a.addClass('current');
        } else {
            $a.removeClass('current');
        }
    });
    $('input[name="limit"]').val(num);
    $('input[name="offset"]').val(0);
    console.log("Setting limit to:" + num);
    list_data_api();
    return false;
}

function SetPage(pagenum) {
    var limit = parseInt($('input[name="limit"]').val());
    var intPagenum = parseInt(pagenum);
    var offset = limit * (intPagenum - 1);
    $('input[name="offset"]').val(offset);
    list_data_api();
    return false;
}

function list_data_api(Mode,Page) {
    var $datatable = $('tbody#datatable');
    var $js_template = $('#tmpl_table').html(); /* шаблон таблицы */
    var $params_form = $('form#params_form'); /* форма с параметрами JSON запроса */

    function Pager(limit, offset, total_count) {
        this.limit = limit || 15;
        this.offset = offset || 0;
        this.total_count = total_count || 0;
        this.total_pages = Math.ceil(this.total_count / this.limit);
        this.current_page = Math.ceil(this.offset / this.limit) + 1
    };


    /* получаем данные из схемы */
    $.ajax({
        tape: 'POST',
        url:  JsonDataUrl,
        dataType: "json",
        data: $params_form.serialize()
    })
    .done(function(result) {
        /* инициализация */

        /* очищаяем таблицу, если она заполнена */
        $datatable.empty();

        /* if (Page == undefined) { $('input[name="page"]').val(1); }   /* устанавливаем страницу на номер 1*/

        /* предворительная обработка result, функция preprocess_result() декларируется в основном скрипте вида, необходима глобальная req_preprocess_result = 1 */
        if (typeof req_preprocess_result != 'undefined' && req_preprocess_result == "1") {
            preprocess_result(result); /* постобработка вынесена из шаблона в функцию*/
        }

        /* Стандартная постобработка */
        if (result.results && result.results.length > 0) {                              /* Если из схемы получены строки ( data json['data'] не пуста )*/
            for (var i = 0,data_len = result.results.length; i < data_len; i++ ) {   /* проходим по массиву данных из схемы result.data */
                var el = result.results[i];
                var tr = Mustache.to_html($js_template, el);  /* создаем шаблонный объект с данными из элемента массива */
                $datatable.append(tr);                               /* вставляем щаблонный объект (строчку) в таблицу */
            }
        }
        /* Постраничная навигация  */
            var page_limit = $('input[name=limit]').val();
            var page_offset = $('input[name=offset]').val();
            var total_count = result.count;
            var pager = new Pager(page_limit, page_offset, total_count);

            // console.log( "[Pager data] Limit: " + pager.limit + " offset: " + pager.offset + " total_count: " + pager.total_count + " total_pages: " + pager.total_pages + " current: " + pager.current_page);

            /* Заполняем пейджинг */
            listing_pager(pager.current_page, pager.total_pages);
            $('span#total_entries > em').html(total_count);
        })
        .fail(function(result) { alert("Error!: "+ result)});
        return false;
}

function ResetFormDefault(formname) {
    document.getElementById(formname).reset();
    list_data_api();
    return false;
}

    function input_autocomplite(input_name, url, model_name, field_name, filter_type){
        var $input = $('input[name=' + input_name+ ']');
        $input.autocomplete({
            source: function(request, response){
                $.ajax({ url: url, dataType: "json", data: { query: request.term, model: model_name, field: field_name, filter_type: filter_type}})
                        .done(function(result)  {
                            var suggestions = [];
                            if (result.data && result.data.length > 0) {
                                for ( var i = 0, data_len = result.data.length; i < data_len; i++ ) {
                                    suggestions.push(result.data[i][0]);
                                }
                                response(suggestions);
                            }
                        })
            }
        });
    }

function SortUpdate(el) {
    var $Thead = $( "table.listing_grid thead a.sortable" );    // Очищаем все ссылки в заголовках от отметки об активном фильтре
        $Thead.removeClass('active');
    $(el).addClass("active");                                   // Устанавливаем класс активный на текущий заголовок
    var SortParam = $(el).attr("rel");
    var $OrderParamInput = $('input[name="ordering"]');
    var CurrentOrderField = $OrderParamInput.val();
    var regex = new RegExp('^(-).*');
        //console.log("SortParam: " + SortParam + " CurrentOrderField: " + CurrentOrderField);
    if (CurrentOrderField.search(SortParam) > -1)  {
        //console.log("Search > - 1");
        if (CurrentOrderField.search(/^-/) > -1) {
            //console.log("- found");
            $OrderParamInput.val(SortParam);
        } else {
            $OrderParamInput.val("-" + SortParam);
        }
    } else {
        //console.log("Sort param not found");
        $OrderParamInput.val(SortParam);
    }
    list_data_api();
    return false;
}

function card($this) {
    var $tr = $($this);
    var id = $($this).date('id');
    // var code = id.replace("linktr",""); //$'
    var url = base_url + "/" + id + "/card/";
    document.location.href = url;
    return false;
}

function highlight_search_results(jsondata, search_string) {
    if (search_string !== undefined && search_string != "") {
        var jresult = JSON.stringify(jsondata, function(k, val) {
                          if (typeof val === 'string' && val != "") {
                              var re = new RegExp(search_string, 'i');
                              val =  val.replace(re, '<b class="search">' + search_string + '</b>');
                          }
                        return val;
                    });
        return JSON.parse(jresult);
    } else {
        return jsondata;
    }
}