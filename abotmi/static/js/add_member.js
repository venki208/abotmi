var csrf_token = $("#id_csrf_token").val();

// adding class to aadhaar otp div
$('#generate_aadhaar_otp').addClass('change_bg_color');
// Attaching country code plugin to mobile number field
$("#mobile").intlTelInput({
    geoIpLookup: function (callback) {
        $.getJSON('http://ipinfo.io', function (resp) {
            var countryCode = (resp && resp.country) ? resp.country : "";
            callback(countryCode);
        });
    },
    nationalMode: false,
    initialCountry: "in",
    separateDialCode: true
});

// showing or hiding divs
function toogle_client_information(id){
    $('.client_information').each(function(index) {
        if ($(this).attr("id") == id) {
            $(this).toggle(200);
        }
        else {
            $(this).hide(600);
        }
     });
}

// Validates the form
function validate_form() {
    missed_form_field = 0;
    var terms_conditions = iagree_validation();
    var email_id = validate_field_onkeypress('primary_email', 'help-text-primary_email', 'Email ID');
    var mobile_number = validate_field_onkeypress('mobile', 'help-text-mobile', 'Mobile Number');
    var last_name = validate_field_onkeypress('last_name', 'help-text-last_name', 'Last Name');
    var first_name = validate_field_onkeypress('first_name', 'help-text-first_name', 'First Name');
    if(first_name !=0
        || last_name != 0
        || mobile_number != 0
        || email_id != 0
        || terms_conditions != 0){
            return false;
    }else{
        return true;
    }
}

// Advisor cancel map with Client if client already Exists in UPLYF
function cancel_map_client(question_div_id) {
    $("#"+question_div_id).addClass('hide');
    $("#save_member_data").prop('disabled', false);
    $("#id_save_continue_add_member").prop('disabled', false);
    $("#add_member_form").trigger("reset");
}

// Resets the add client form
function reset_add_client_form(id) {
    $("#"+id)[0].reset();
    cancel_map_client('id_advisor_conformation');
    document.getElementById('name_div').style.display = 'none';
    document.getElementById('aadhaar_div').style.display = 'none';
    document.getElementById('agree_div').style.display = 'none';
    document.getElementById('save_member_div').style.display = 'none';
    document.getElementById('id_advisor_authorisation').style.display = 'block';
    document.getElementById('aadhaar_submit_btn_div').style.display = 'none';
}

function move_text_to_center(div_id, text_id) {
    var elem = document.getElementById(text_id);
    var pos = 0;
    var id = setInterval(frame, 1);
    function frame() {
        if (pos >= $("#"+div_id).width()/2.7) {
            clearInterval(id);
        } else {
            pos++;
            elem.style.left = pos + 'px';
        }
    }
}

// Shows the success message
function show_success_message(message) {
    $("#add_member_form").trigger('reset');
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-success');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
    $("#id_success_alert").fadeIn( 450 ).delay( 5000 ).fadeOut( 400 );
}

// Shows the error message
function show_error_message(message) {
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-danger');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
    $("#id_success_alert").fadeIn( 450 ).delay( 6000 ).fadeOut( 400 );
}

// Shows the warning message
function show_warning_message(message) {
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-warning');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
    $("#id_success_alert").fadeIn( 450 ).delay( 6000 ).fadeOut( 400 );
}

// Shows the conformation message
function show_conformation_alert(email) {
    $("#id_advisor_conformation").removeClass('hide');
    $("#save_member_data").prop('disabled', true);
    $("#id_save_continue_add_member").prop('disabled', true);
    $("#id_map_client_button").attr('onclick',  'accept_mapping("'+email+'",'+'"'+'accepted'+'"'+');');
    $("#id_cancel_client_button").attr('onclick', 'cancel_map_client("id_advisor_conformation");');

}

// Validates the confirmation
function iagree_validation(){
    var missed_field = 0;
    if(document.getElementById("iagree").checked == true){
        document.getElementById('iagree').style.border='';
        document.getElementById('help-text-iagree').innerHTML='';
    }else{
        document.getElementById('iagree').style.border='1px solid #C32F2F';
        document.getElementById('help-text-iagree').innerHTML='Please agree to the declaration';
        $("#iagree").focus();
        missed_field = 1;
    }
    return missed_field;
}

// Validating Adhaar number field
function validateAadhar(str) {
    var re = /^\d{12}$/;
    var aadhar = document.getElementById(str);
    if (!aadhar.value.match(re)) {
        document.getElementById(str).value = "";
        alert("Enter Valid Aadhar number");
    }
}

// checking and validating input value is string or not
function validateAlpha(str) {
    var name = document.getElementById(str);
    var alpha = /^[a-zA-Z()\s]+$/.test(name.value);
    if (alpha) { return true; }
    else {
        document.getElementById(str).value = "";
        alert("Enter valid Input");
    }
}

// Validating the aadhar number
function validate_aadhar(id) {
    var aadhar_number = document.getElementById(id).value;
    var no_format = /^(\d{12})$/;
    user_aadhaar = user_aadhaar;
    if (aadhar_number != '') {
        if (!aadhar_number.match(no_format)) {
            document.getElementById('aadhar_number').value = "";
            document.getElementById('aadhar_number').style.border = '1px solid #C32F2F';
            document.getElementById('help-text-aadhar_number').innerHTML = 'Please enter 12 digits Aadhaar number';
            $("#aadhar_number").focus();
        } else {
            if (aadhar_number.length < 11 || aadhar_number.length > 12) {
                document.getElementById('aadhar_number').value = "";
                document.getElementById('aadhar_number').style.border = '1px solid #C32F2F';
                document.getElementById('help-text-aadhar_number').innerHTML = 'Please enter 12 digits Aadhaar number';
                $("#aadhar_number").focus();
            } else {
                if (aadhar_number < 99999999999) {
                    document.getElementById('aadhar_number').value = "";
                    document.getElementById('aadhar_number').style.border = '1px solid #C32F2F';
                    document.getElementById('help-text-aadhar_number').innerHTML = 'Please Enter valid Aadhaar Number.';
                    $("#aadhar_number").focus();
                }
                else if (user_aadhaar == aadhar_number) {
                    document.getElementById(id).value = "";
                    document.getElementById('help-text-' + id).innerHTML = "You cannot use your aadhaar number for your clients.Please use clients aadhaar number.";
                }
                else {
                    document.getElementById('aadhar_number').style.border = '';
                    document.getElementById('help-text-aadhar_number').innerHTML = '';
                }
            }
        }
    }
}

/**
 * @use: Validating the advisor email id and add client form email id
 *      advisor can't add him as client
 */
function validateEmail_id(id) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    var email = document.getElementById(id);
    var email1 = email1;
    if (!re.test(email.value)) {
        document.getElementById(id).value = "";
    }
    else if (email1 == email.value) {
        document.getElementById('help-text-' + id).innerHTML = "You can not add Yourself";
        document.getElementById(id).value = "";
    }

    else {
        document.getElementById('help-text-' + id).innerHTML = "";
    }
}

// Adding Client in uplyf
function save_member_data(id) {
    var token = csrf_token;
    var validation_result = validate_form();
    var email = $('#primary_email').val();
    if (validation_result) {
        $.ajax({
            type: 'POST',
            url: '/dashboard/save_new_members/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                first_name: $('#first_name').val(),
                last_name: $('#last_name').val(),
                email: email,
                mobile: $("#mobile").val(),
            },
            success: function (response) {
                if (response == 'User already exists') {
                    show_conformation_alert(email);
                } else if (response == 'You have already added') {
                    $("#help-text-primary_email").html('You have already Added');
                    $("#primary_email").addClass('not_valid');
                    $("#primary_email").focus();
                } else if (response == 'Member Rejected') {
                    show_error_message("<strong>Member Rejected&nbsp;</strong> You can't add.");
                }
                else if (response == 'Waiting for user approval') {
                    show_warning_message("<strong>Waiting for Member Approval!&nbsp;</strong> You  have sent request already.")
                }
                else if (response == 'User Created') {
                    show_success_message('<strong>Successful!&nbsp;</strong> You have Added one.');
                }
                else if (response == 'unable to save') {
                    alert('unable to add member');
                }
                else if (response == 'User is an Advisor') {
                    $("#help-text-primary_email").html('The advisor is already exist in our system');
                    $("#primary_email").focus();
                }
                else {
                    show_success_message('<strong>Successful!&nbsp;</strong>' + response);
                }
            },
            error: function (response) {
                alert('unable to add member');
            }
        });
    }
}

// Adding mapping between uplyf client and upwrdz advisor
function accept_mapping(user_email, status) {
    var token = csrf_token;
    $.ajax({
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader('X-CSRFToken', token);
        },
        url: "/dashboard/advisor_member_maping/",
        data: {
            'user_email': user_email,
            'accepted': status
        },
        success: function (response) {
            cancel_map_client('id_advisor_conformation');
            if (response == 'Mail send') {
                show_success_message('<strong>Successful!&nbsp;</strong> Email sent for Approval.');
            }
        },
        error: function (response) {
            alert('unable to Map Client');
        }
    });
}

// Submitting Addhar form for getting OTP
function got_to_send_otp() {
    var token = csrf_token;
    var terms_conditions = iagree_validation();
    var validate_adhar = validate_field_onkeypress(
        'aadhar_number', 'help-text-aadhar_number', 'aadhar_number');
    if (!terms_conditions && validate_adhar == 0) {
        var aadhaar_no = $("#aadhar_number").val();
        if (aadhaar_no.length == 12) {
            $.ajax({
                type: "POST",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                url: "{% url 'aadhaar:check_aadhaar_present'%}",
                data: { "aadhaar_no": aadhaar_no },
                success: function (data) {
                    $form = $("<form action='https://prod.aadhaarbridge.com/kua/_init' method='post' id='adhaar_form'></form>");
                    var adhaar_form = $("#adhaar_form");
                    $.each(data, function (KEY, VALUE) {
                        adhaar_form.append("<input type='hidden' name='" + KEY + "' value='" + VALUE + "'>");
                    })
                    $("#adhaar_form").submit();
                },
                error: function (res, textStatus, errorThrown) {
                    if (res.status == 401) {
                        $("#aadhar_number").val("");
                        alert(res.responseJSON.data);
                    }
                    if (res.status == 400) {
                        $("#aadhar_number").val("");
                        alert(res.responseJSON.data);
                    }
                }
            });
        } else {
            alert("invalid aadhaar number");
        }
    }
}

// by default showing add client kyc form
$(document).ready(function (e) {
    $('[name="cancel_button"]').click();
});

// Showing add client KYC form
function no_auth_button(formId) {
    document.getElementById('name_div').style.display = 'block';
    document.getElementById('aadhaar_div').style.display = 'none';
    document.getElementById('aadhaar_submit_btn_div').style.display = 'none';
    document.getElementById('agree_div').style.display = 'block';
    document.getElementById('save_member_div').style.display = 'block';
    document.getElementById('id_advisor_authorisation').style.display = 'none';
}

// Showing Aadhar form
function yes_auth_button(formId) {
    document.getElementById('name_div').style.display = 'none';
    document.getElementById('aadhaar_div').style.display = 'block';
    document.getElementById('aadhaar_submit_btn_div').style.display = 'block';
    document.getElementById('agree_div').style.display = 'block';
    document.getElementById('save_member_div').style.display = 'none';
    document.getElementById('id_advisor_authorisation').style.display = 'none';
}