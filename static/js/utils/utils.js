
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
