// Validating the form by passing id of input field
function validate_input(id) {
    if (id == 'company_url') {
        var domain = document.getElementById(id).value;
        var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
        if (!domain.match(re)) {
            $('#help-text-' + id).html('Please enter valid company URL');
            document.getElementById(id).value = '';
            return false;
        } else {
            $('#' + id).removeClass('not_valid');
            $('#help-text-' + id).html('');
        }
    } else if (id == 'point_of_contact_email_id' || id == 'id_final_company_email') {
        var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        var email = document.getElementById(id).value;
        if (!re.test(email)) {
            document.getElementById('point_of_contact_email_id').value = "";
            $('#help-text-point_of_contact_email_id').html("Please enter valid email ID");
            $("#point_of_contact_email_id").focus();
            return false;
        } else {
            check_email_exist_or_not(id, 'point_of_contact_email_id');
        }
    } else if (id == 'point_of_contact_name') {
        var name = document.getElementById(id);
        if (name.value != '') {
            var alpha = /^[a-zA-Z()\s]+$/.test(name.value);
            if (alpha) {
                $('#' + id).removeClass('not_valid');
                $('#help-text-' + id).html('');
            } else {
                document.getElementById(id).value = "";
                $('#help-text-' + id).html('Enter Valid Input');
                return false;
            }
        }
    } else if (id == 'point_of_contact_phone_number') {
        var re = /^\d{10}$/;
        var mobile = document.getElementById(id);
        if (!mobile.value.match(re)) {
            document.getElementById(id).value = "";
            $('#help-text-' + id).html("Please enter valid mobile number");
        } else {
            $('#' + id).removeClass('not_valid');
            $('#help-text-' + id).html('');
        }
    } else {
        try {
            $('#' + id).removeClass('not_valid');
            $('#help-text-' + id).html('');
        } catch (e) { }
    }
}

// Checking email is exists or not
function check_email_exist_or_not(id, input_id) {
    $.ajax({
        type: 'POST',
        url: "/company/check_email_exist_or_not/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: { 'username': $("#" + id).val(), value: 'company_reg' },
        success: function (response) {
            if (response == 'new_user' || response == 'user_email') {
                $('#' + input_id).removeClass('not_valid');
                $('#help-text-' + input_id).html('');
                $("#id_final_company_email").val($("#" + id).val());
            } else {
                $('#' + input_id).val('');
                $('#' + input_id).addClass('not_valid');
                $('#help-text-' + input_id).html('Email ID already exists');
            }
        },
        error: function (response) {
        }
    });
}