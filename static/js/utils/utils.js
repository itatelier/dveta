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

function add_contact(company_id, contact_id) {
    $.ajax({
        type: 'GET',
        url:  '/persons/create_company_contact_json/',
        dataType: "json",
        data: { 'company_id': company_id, 'contact_id': contact_id}
    })
    .done(function(result){
        if (result.result == "1") {
            location.reload()
        }
        console.log("Result");
    });
    return false;
};

function CheckPhoneInput(company_id, obj) {
            var $input_object = $(obj);
            var number = $input_object.val();
            console.log(number);
            if (number.length == 10) {
                console.log("Value: " + this.value);
                $.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});
                $.ajax({
                    url:  '/persons/api/contacts_search_json/',
                    dataType: "json",
                    data: { 'contact__phonenumber': number}
                })
                .done(function(result) {
                    if (result.count > 0) {
                        var name = result.results[0].contact.person.nick_name;
                        var contact_id = result.results[0].contact.id;
                        var person_id = result.results[0].contact.person.id;
                        var comment = result.results[0].contact.comment;
                        var result_company_id = result.results[0].company;
                        var ErrorString = "";
                        if (company_id == result_company_id) {
                            ErrorString = 'Контакт c номером '+ number +' уже привязан к клиенту!';
                        } else {
                            ErrorString = 'Номер '+number+' уже есть в контакте <a href="/persons/'+ person_id +'/card/">'+name+'</a>, добавить контакт вместо нового? <a href="#" onClick="add_contact('+company_id+', '+contact_id+');">Да</a>';
                        }
                        $('<em>' + ErrorString + '</em>').insertAfter($input_object);
                        $input_object.val('');
                        $input_object.focus();
                    } else {
                        $input_object.addClass('lightgreen_bg');
                    }
                })
                .fail(function(result) { console.log("Error! result: "+ result)});
            }
};