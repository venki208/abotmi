var csrf_token = $("#id_csrf_token").val();

// Sending OTP 
function send_otp(medium, email=undefined, name=undefined, mobile=undefined) {
    if (!email){
        var email = $("#email").val();
    }
    if(!name){
        var name = $("#name").val();
    }
    if(!mobile){
        var mobile = get_mobile_no("#mobile");
    }
    var medium = medium;
    $.ajax({
        type: 'POST',
        url: '/signup/send_otp/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data: {
            mobile: mobile,
            email: email,
            name: name,
            medium: medium
        },
        complete: function (e, xhr, settings) {
            var status = e.status;
            if (status == 200) {
                $("#otp_verified_message_model").modal({
                    show: true,
                    keyboard: false,
                    backdrop: 'static'
                });
            }
            else {
                alert(" Unable to send ");
            }
        }
    });
}

// Validating the OTP form
function validate_otps() {
    var missed_field = 0;
    if (email_signup == "None") {
        if ($("#id_email_otp").val() == '') {
            $('#help_text_id_email_otp').html('Please Enter Email OTP');
            $("#id_email_otp").focus();
            missed_field = 1;
        }
    }
    if ($("#id_otp").val() == '') {
        $('#help_text_id_otp').html('Please Enter Mobile OTP');
        $("#id_otp").focus();
        missed_field = 1;
    }
    if (missed_field == 0) {
        return true;
    } else {
        return false;
    }
}

// Verifing the OTP and submitting the OTP
function verify_and_submit_otp(){
    if (validate_otps()) {
        return $.ajax({
            type: 'POST',
            url: '/signup/verify_otp/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: {
                otp: $("#id_otp").val(),
                email_otp: $('#id_email_otp').val(),
            }
        });
    }else{
        return false;
    }
}