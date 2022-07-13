// Send Profile Link Modal
function add_mail_fields() {
    var result_add_fields = json_output_result();
    if (result_add_fields[1] <= 0) {
        id_modal++;
        $('<div class="border_title row m-0" id="additional_div' + id_modal + '">' +
            '<div class="col-md-12" id="id_border_line" style="padding-top:10px;">'+
                '<hr style="border-color: #070147;border-width: 3px;max-width: 100%;">'+
                '<a type="button" class="btn pull-right" id="additional_div' + id_modal + '" name="additional_div' + id_modal + '" onclick=remove_row(id);> <i class="fa fa-times"></i></a>' +
            '</div>'+
            '<div class="col-md-3">'+
                '<label class="control-label">Title</label>'+
                '<select class="form-control" id="id_title' + id_modal + '" name="title' + id_modal + '">'+
                    '<option value="Select">Select</option>'+
                    '<option value="Mr">Mr</option>'+
                    '<option value="Ms">Ms</option>'+
                    '<option value="Dr">Dr</option>'+
                    '<option value="Prof">Prof</option>'+
                '</select>'+
            '</div>'+
            '<div class="col-md-4">'+
                '<label class="control-label">Name</label>'+
                '<input type="text" class="form-control" name="name' + id_modal + '" id="id_name' + id_modal + '" placeholder="Name">'+
            '</div>'+
            '<div class="col-md-5">'+
                '<label class="control-label">Email Id</label>'+
                '<input type="text" class="form-control" name="email' + id_modal + '" id="id_email' + id_modal + '" placeholder="Email Id">'+
            '</div>'+
            '<div class="col-md-12">'+
                '<label class="control-label">Subject</label>'+
                '<input type="text" class="form-control" name="subject' + id_modal + '" id="id_subject' + id_modal + '" placeholder="Subject">'+
            '</div>'+
            '<div class="col-md-12">'+
                '<label class="control-label">Message</label>'+
                '<textarea class="form-control" rows="4" cols="50" id="id_mail_body_content' + id_modal + '" name="mail_body_content' + id_modal + '">' + advisor_name + ' has shared profile for your referenceee.</textarea>'+
            '</div>'+
        '</div>').appendTo(add_fields);
    }
}

// Removing Additional Email divs
function remove_row(id) {
    $("#" + id).remove();
}

// Validating and returning json data
function json_output_result() {
    var link = profile_link;
    var input_ids, values;
    var input_values = [];
    var i = 0;
    var validation_id = 0;
    var $inputs = $('#add_fields :input');
    $inputs.each(function (index) {
        input_ids = $(this).attr('id');
        values = $("#" + input_ids).val();
        values = values.trim();
        input_values[i] = $(this).attr('name') + ":" + values + ",";
        if (i == 0 || (i % 5 == 0)) {
            if (values == '' || values == 'Select') {
                validation_id = +1;
                alert('Please Select Title');
                $("#" + input_ids).focus();
                return false;
            } else {
                input_values[i] = '"title"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 1 || (i % 5 == 1)) {
            if (values == '') {
                validation_id = +1;
                alert('Please Enter Name');
                $("#" + input_ids).focus();
                return false;
            } else {
                var alpha = /^[a-zA-Z()\s]+$/.test(values);
                if (!alpha) {
                    alert('Please Enter Valid Name');
                    $("#" + input_ids).focus();
                    validation_id = +1;
                    return false;
                }
                input_values[i] = '"name"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 2 || (i % 5 == 2)) {
            if (values == '') {
                validation_id = +1;
                alert('Please Enter Email');
                $("#" + input_ids).focus();
                return false;
            } else {
                var email_valid = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
                if (!email_valid.test(values)) {
                    alert('Please Enter Valid Email');
                    $("#" + input_ids).focus();
                    validation_id = +1;
                    return false;
                }
                input_values[i] = '"email"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 3 || (i % 5 == 3)) {
            if (values == '') {
                validation_id = +1;
                alert('Please Enter Subject');
                $("#" + input_ids).focus();
                return false;
            } else {
                input_values[i] = '"subject"' + ":" + '"' + values + '"' + ",";
            }
        }
        if (i == 4 || (i % 5 == 4)) {
            if (values == '') {
                validation_id = +1;
                alert('Please Enter Message');
                $("#" + input_ids).focus();
                return false;
            } else {
                main_mail_body_content = values.replace(/(?:\r\n|\r|\n)/g, '<br />');
                input_values[i] = '"mail_body"' + ":" + '"' + main_mail_body_content + link + '"';
            }
        }
        i++;
    });

    var json_index = 0;
    var json_output = [];
    var output = '{';
    for (var i = 0; i < input_values.length; i++) {
        var output = output + input_values[i];
        if ((i + 1) % 5 == 0 && i != 0) {
            var output = output + '}';
            json_output[json_index] = output;
            json_index++;
            var output = '{';
        }
    }
    json_final_output = [json_output, validation_id]
    return json_final_output;
}

// Sending profile link to emails
function send_profile_mail_id(id) {
    var token = csrf_token;
    if (id == 'id_send_mail_cancel') {
        var remove_ids = $(".remove-button").parent().map(function () {
            return this.id;
        }).get();
        for (i = 0; i < remove_ids.length; i++) {
            $('#' + remove_ids[i]).parent().remove();
        }
        var $inputs = $('#add_fields :input[type="text"]');
        $inputs.each(function (index) {
            var ids_email_body = $(this).attr('id');
            $('#' + ids_email_body).val('');
        });
        $('#id_title1').val('Select');
    }
    else {
        var json_output_value = json_output_result();
        if (json_output_value[1] <= 0) {
            document.getElementById('id_send_button').innerHTML = 'Sending ...';
            $('#id_send_button').prop('disabled', true);
            $.ajax({
                method: "POST",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                url: "/my_identity/share_profile_by_email/",
                data: {
                    value: '[' + json_output_value[0] + ']'
                },
                success: function (response) {
                    if (response == 'success') {
                        show_alert(
                            'success',
                            'share_profile_by_email',
                            '<p>Email has been sent successfully</p>'
                        );
                    }else{
                        show_alert(
                            'error',
                            'share_profile_by_email',
                            '<p>Unable to send Email right now.\n \nPlease try again after some time</p>'
                        );
                    }
                },
                error: function (response) {
                    show_alert(
                        'error',
                        'share_profile_by_email',
                        '<p>Unable to send Email right now.\n \nPlease try again after some time</p>'
                    );
                },
            });
        }
    }
}