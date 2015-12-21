/* Функция добавления 0 к цифре */
function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}
/* Переводим даты из формата 2013-03-29T07:18:00Z  => year, month, date[, hours, minutes, seconds, ms]*/
function date_json2hr(str_date_json_format) {

    var date_split = str_date_json_format.match(/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/);
    var dt_object = new Date(date_split[1], date_split[2]-1, date_split[3], date_split[4], date_split[5]);
    var return_obj = {};
    var date_str = zeroPad(dt_object.getDate(),2);
    var month_str = zeroPad(dt_object.getMonth() + 1,2);
    var year_str = zeroPad(dt_object.getYear() - 100+2000,2);
    var hours_str = zeroPad(dt_object.getHours(),2);
    var minutes_str = zeroPad(dt_object.getMinutes(),2);
    var date = date_str + "-" + month_str + "-" + year_str;
    var time = hours_str + ":" + minutes_str;
    return_obj.date = date;
    return_obj.time = time;
    return return_obj;
}

function date_json2dt(str_date_json_format, offset_param) {
    var date_split = str_date_json_format.match(/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/);
    var dt_out = new Date(date_split[1], date_split[2] - 1, date_split[3], date_split[4], date_split[5]);
    if (offset_param) {
        if (offset_param.way === '+' ) {
            dt_out.setDate(dt_out.getDate() + offset_param.size_days);
        } else if (offset_param.way === '-') {
            dt_out.setDate(dt_out.getDate() - offset_param.size_days);
        }
    }
    // console.log('Date out:' + dt_out.toString('dd.MM.yyyy'));
    return dt_out;
}
