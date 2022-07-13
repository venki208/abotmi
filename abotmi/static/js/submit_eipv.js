//Global variable declaration and initializing
var csrf_token = $("#id_csrf_token").val();
var search_data = [];
var is_match_string = false;
var arr_val;
var profile_id;
var params;

$("#id_mobile_otp_advisor_resend")
    .removeAttr('onclick')
    .bind('click', [user_profile_id, 'mobile'], resend_mobile_otp);
    
$("#id_email_otp_advisor_resend")
    .removeAttr('onclick')
    .bind('click', [user_profile_id, 'email'], resend_mobile_otp);

$("#id_submit_advisor_otp_email")
    .removeAttr('onclick')
    .bind('click', [user_profile_id, 'email'], verify_otp_data);

$("#id_submit_advisor_otp_mobile")
    .removeAttr('onclick')
    .bind('click', [user_profile_id, 'mobile'], verify_otp_data);
    
$("#id_submit_advisor_otp")
    .removeAttr('onclick')
    .bind('click', [user_profile_id], submit_eipv);

$(document).ready(function() {
    $('#id_mobile_otp_advisor').bind('paste', function (e) {
        var mobiles = e.originalEvent.clipboardData.getData('Text').trim();
        if (user_agent_country == "IN") {
            if (mobiles.length) {
                $('#id_submit_advisor_otp_mobile').prop('disabled', false);
                $('#id_submit_advisor_otp_mobile').removeClass('upwrdz-button-verify');
            } else {
                $('#id_submit_advisor_otp_mobile').prop('disabled', true);
            }
        }
    });
    $('#id_email_otp_advisor').bind('paste', function (e) {
        var emails = e.originalEvent.clipboardData.getData('Text').trim();
        if (emails.length) {
            $('#id_submit_advisor_otp_email').prop('disabled', false);
            $('#id_submit_advisor_otp_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_advisor_otp_email').prop('disabled', true);
        }
    });
    $("#mobile").intlTelInput({
        nationalMode: false,
        initialCountry: user_agent_country,
        separateDialCode: true,
    });
    set_address("#address1", address1);
});

$(document).ready(function () {
    $('.nav-tabs > li a[title]').tooltip();

    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        var $target = $(e.target);
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {
        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);
        $('.wizard .nav-tabs li.active .connecting-line').css({
            "border-bottom-left-radius": 0,
            "border-top-left-radius": 0
        });
        enable_eipv_submit();
    });
    $(".prev-step").click(function (e) {
        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);
        enable_eipv_submit();
    });
});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}

function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

$(document).ready(function () {
    // if (advisors) {
    //     $("#email_otp_block").hide();
    // }
});

// Validates and submit the form
function submit_forms(){
    var missed_field = 0;
    if($('#mobile').intlTelInput("isValidNumber") == false){
        $('#help_text_mobile').html('Please Enter Mobile Number');
        $("#mobile").focus();
        missed_field = 1;
    }
    if($("#country").val() == ''){
        $('#help-text-country').html('Please Select Country');
        $("#country").focus();
        missed_field = 1;
    }
    if(validate_field_onkeypress('pincode', 'help_text_pincode', 'Pincode') && user_agent_country =='IN'){
        $('#help_text_pincode').html('Please Enter Valid Code');
        $("#pincode").focus();
        missed_field = 1;
    }
    if($("#zipcode").val() == '' && user_agent_country != 'IN'){
        $('#help_text_zipcode').html('Please Enter Code ');
        $("#zipcode").focus();
        missed_field = 1;
    }
    if($("#city").val() == ''){
        $('#help_text_city').html('Please Enter City ');
        $("#city").focus();
        missed_field = 1;
    }
    if (validate_field_onkeypress('address1', 'help_text_address', 'address1')) {
        missed_field = 1;
    }
    if ($("#name").val() == '') {
        $('#help_text_first_name').html('Please Enter first Name');
        $("#name").focus();
        missed_field = 1;
    }
    if ($("#last_name").val() == '') {
        $('#help_text_last_name').html('Please Enter last Name');
        $("#last_name").focus();
        missed_field = 1;
    }
    if ($("#suffix").val() == 'Select' || $("#suffix").val() == '') {
        $('#help_text_suffix').html('Please Select Title');
        $("#suffix").focus();
        missed_field = 1;
    }
    if(missed_field==0){
        if (user_agent_country !="IN"){
            $("#advisor_mobile_otp_block").hide();
            var mode_type = 'email';
        }else{
            $("#advisor_mobile_otp_block").show();
            var mode_type = 'both';
        }
        if (user_email_status == "True" && user_agent_country != "IN"){
            submit_eipv();}
        else{ show_verify_otp_modal(mode_type);}
        // if ($("#country").val()=="India"){show_verify_otp_modal();}
    }
}

//Fucntion sents the OTP
function resend_mobile_otp(params) {
    if (params.data){
        datas = params.data;
        var id = datas[0];
        var mode = datas[1];
    }else{
        var id = params[0];
        var mode = params[1];
    }
    $.ajax({
        method: 'POST',
        url: '/login/resend_otp/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: { 'profile_id': id, 'mode': mode },
        success: function (e, xhr, settings) {
            if ((settings.status == 200) && (mode=="mobile")) {
                $("#advisor_mobile_otp_success_text")
                    .fadeIn()
                    .fadeOut(5000, 'swing');
            }
            else if ((settings.status == 200) && (mode == "email")) {
                $("#advisor_email_otp_success_text")
                    .fadeIn()
                    .fadeOut(5000, 'swing');
            }
            else{
                $("#advisor_mobile_otp_success_text")
                    .fadeIn()
                    .fadeOut(5000, 'swing');
            }
        }
    });
}

// function for load otp modal
function show_verify_otp_modal(mode) {
    $("#signup-login-modal").modal('hide');
    $("#advisor_otp_verified_message_model").modal({
        'show': true,
        'keyboard': false,
        'backdrop': 'static'
    });
    params = [user_profile_id, mode];
    resend_mobile_otp(params);
}

function validate_mobile_otp(){
    var mobiles = $('#id_mobile_otp_advisor').val().trim();
    if (user_agent_country == "IN") {
        if (mobiles.length>0){
            $('#id_submit_advisor_otp_mobile').prop('disabled', false);
            $('#id_submit_advisor_otp_mobile').removeClass('upwrdz-button-verify');
        }else{
            $('#id_submit_advisor_otp_mobile').prop('disabled', true);
        }
    }
}   

function validate_email_otp() {
    var emails = $('#id_email_otp_advisor').val().trim();
    if (user_agent_country == "IN") {
        if (emails.length >0 && user_email_status != true) {
            $('#id_submit_advisor_otp_email').prop('disabled', false);
            $('#id_submit_advisor_otp_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_advisor_otp_email').prop('disabled', true);
        }
    } else if (user_agent_country != "IN") {
        if (emails.length >0 && user_email_status != true) {
            $('#id_submit_advisor_otp_email').prop('disabled', false);
            $('#id_submit_advisor_otp_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_advisor_otp_email').prop('disabled', true);
        }
    }
}


// Validates the OTP form
function validate_otp_form() { 
    var validate_email_otp = 0;
    var validate_mob_otp = 0;
    var selected_country = $("#country").val();
    validate_mob_otp = validate_field_onkeypress(
        'id_mobile_otp_advisor', 'help_text_id_mobile_otp_advisor', ' Mobile OTP');
    validate_email_otp = validate_field_onkeypress(
        'id_email_otp_advisor', 'help_text_id_email_otp_advisor', ' Email OTP');
    if(user_agent_country =="IN"){
        if (validate_mob_otp != 0 && validate_email_otp !=0) {
            return false;
        } else {
            return true;
        }
    }else if (user_agent_country !="IN"){
        if(validate_email_otp !=0 ){
            return false;
        } else {
            return true;
        }
    } 
    else {
        return false;
    }
}

// It verifies the otp profile_id
function verify_otp_data(params) {
    var id = params.data[0];
    var otp_form_valid_result = validate_otp_form();
    if (otp_form_valid_result) {
        return $.ajax({
            method: 'POST',
            url: '/login/validate_otp/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: {
                'email_otp': $("#id_email_otp_advisor").val(),
                'mobile_otp': $("#id_mobile_otp_advisor").val(),
                'profile_id': id
            }, 
            success: function (e, xhr, settings) {
            if (settings.status == 200) {
                if (e.email_verf_stat && e.mob_verf_stat) {
                    $('#email-otp-verify-btn-div').addClass('hide');
                    $('#mobile_otp_verified').removeClass('hide');
                    $('#mobile-otp-verify-btn-div').addClass('hide');
                    $('#email_otp_verified').removeClass('hide');
                    $('#id_submit_advisor_otp').prop('disabled', false);
                    $('#back_btn').prop('disabled', true);
                    $('#id_submit_advisor_otp').removeClass('upwrdz-button-verify');
                } else if (e.mob_verf_stat && user_email_status) {
                    $('#mobile-otp-verify-btn-div').addClass('hide');
                    $('#mobile_otp_verified').removeClass('hide');
                    $('#id_submit_advisor_otp').prop('disabled', false);
                    $('#back_btn').prop('disabled', true);
                    $('#id_submit_advisor_otp').removeClass('upwrdz-button-verify');
                } else if (e.email_verf_stat && user_agent_country != "IN") {
                    $('#email-otp-verify-btn-div').addClass('hide');
                    $('#email_otp_verified').removeClass('hide');
                    $('#id_submit_advisor_otp').prop('disabled', false);
                    $('#back_btn').prop('disabled', true);
                    $('#id_submit_advisor_otp').removeClass('upwrdz-button-verify');
                }
                if (e.mob_verf_stat == false) {
                    $("#help_text_id_mobile_otp_advisor").html('Please enter valid OTP');
                }
                if (e.email_verf_stat == false) {
                    $("#help_text_id_email_otp_advisor").html('Please enter valid OTP');
                }
            }
        }
        });
    } else {
        return false;
    }
}


//submit the otp and login 
function submit_otp(params){
    var id = params.data[0];
    var verify_otp_result = verify_otp_data(id);
    if (verify_otp_result) {
        verify_otp_result.success(function (e, xhr, settings) {
            if ((settings.status == 200 && e.mob_verf_stat && e.email_verf_stat && user_agent_country == "IN") || (
                user_agent_country != "IN" && settings.status == 200 && e.email_verf_stat)||(
                settings.status == 200 && e.user_source_media != 'signup_with_email' && e.email_verf_stat
                )) {
                $.ajax({
                    method: 'POST',
                    url: '/login/verify_otp_and_login/',
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                    },
                    data: {
                        'email_otp': $("#id_email_otp_advisor").val(),
                        'mobile_otp': $("#id_mobile_otp_advisor").val(),
                        'profile_id': id
                    },
                    success: function (e, xhr, settings) {
                    if (settings.status == 200) { 
                        submit_eipv();
                    } else {
                        alert('Unable to process your request \n Please try again after some time');
                    }
                }
            });
            } if (e.mob_verf_stat == false) {
                $("#help_text_id_mobile_otp_advisor").html('Please enter valid OTP');
            }
            if (e.email_verf_stat == false) {
                $("#help_text_id_email_otp_advisor").html('Please enter valid OTP');
            }
        });
    }
}

// submit the eipv
function submit_eipv() {
    if ((user_mobile_status && user_email_status && user_agent_country == "IN") || (user_email_status && user_agent_country != "IN")) {
        $.ajax({
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            url: '/signup/submit_eipv/',
            data: {},
            success: function (e, xhr, settings) {
                if(settings.status==200){
                    submit_registration_form();
                } else {
                    alert('Unable to process your request \n Please try again after some time');
                }
            }
        });
    }
}

//Submit the personal information registration from 
function submit_registration_form(){
    $.ajax({
        method : 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        url: '/signup/personal_info_forms/',
        data:{
            'suffix' : $("#suffix").val(),
            'name' : $("#name").val(),
            'last_name' : $("#last_name").val(),
            'mobile' : get_mobile_no('#mobile'),
            'address1' : get_address("#address1"),
            'city' : $("#city").val(),
            'country': $("#country").val(),
            'pincode' : $("#pincode").val(),
            'zipcode' : $("#zipcode").val()
        },
        success: function (response) {
            if (response == "True" && user_email_status != "True") {
                $("#advisor_otp_verified_message_model").modal('hide');
                $("#e_ipv_logout_alert_message_model").modal({
                    'show': true,
                    'keyboard': false,
                    'backdrop': 'static'
                });
            }else{
                window.location.href = '/advisor_check/get_advisor_card/';
            }
        },
        error: function (response) {
            alert('Unable to Complete Registration. \n Please try again after some time');
        }
    });
}

// Pincode search functionality
$("input#pincode").autocomplete({
    source: function (request, response) {
        for(arr_val in search_data){
            if (String(search_data[arr_val]).indexOf(String(request.term)) >= 0){
                is_match_string = true;
                break;
            }else{
                is_match_string = false;
            }
        }
        if (is_match_string){
            response(search_data);
        }else{
            $.ajax({
                dataType: "json",
                type: 'POST',
                global: false,
                url: '/signup/search_pincode/',
                beforeSend: setHeader,
                data: {
                    s_key: $('#pincode').val()
                },
                success: function (data) {
                    search_data = $.map(data.pincodes, function (item) {
                        return [String(item.pin_code)];
                    });
                    response(search_data);
                },
                error: function (data) {

                }
            });
        }
    },
    minLength: 3,
    autoFocus: true,
    select: function (event, ui) {
        event.preventDefault();
        $(this).val(ui.item.value);
        search_data = [];
    }
});

//Save the mobile number 
function onchange_mobile_save(id,help_id,field_name) {
    var mobile_no = $('#'+id).intlTelInput("isValidNumber");
    if(mobile_no == false){
        document.getElementById('mobile').style.border='1px solid #C32F2F';
        document.getElementById('help_text_mobile').innerHTML='Enter valid Mobile Number';
        $("#mobile").focus();
        value = document.getElementById('mobile').value = "";
    }else{
        $.ajax({
            url:"/signup/onchange_save_field/",
            method: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token );
            },
            data :{
                username : username,
                value : $('#'+id).intlTelInput("getNumber"),
                'name' : 'mobile'
            },
            success:function(response){
            },
            error:function(response){
            },
        });
    }
}

function validate_login() {
    var is_login_recaptcha = validate_recptcha(login_recaptcha, 'help_login_recpatcha');
    var is_password = validate_field_onkeypress('password', 'help_password', 'Password');
    var is_username = validate_field_onkeypress('username', 'help_username', 'Email');
    if (is_username != 0 || is_password != 0 || is_login_recaptcha != true) {
        return false;
    } else {
        return true;
    }
}

function show_login_modal() {
    $("#e_ipv_logout_alert_message_model").modal('hide');
    $("#message_model").modal({
        'show': true,
        'keyboard': false,
        'backdrop': 'static'
    });
}

// function to load login_user function on click of Sign In button of login modal form
login_submit.click(function () {
    login_user();
});

// function for user login
function login_user() {
    var token = csrf_token;
    var is_valid = validate_login();
    if (is_valid){
        $.ajax({
            url: '/login/user_login/',
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                username: $('#login_form').find('#username').val(),
                password: $('#login_form').find('#password').val(),
            },
            success: function (response) {
                if (response.status == 'true') {
                    $('#error_msg').html('');
                    window.location.href = response.next;
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == 403) {
                    alert('You might have already loggedin \n Please Wait we are refreshing your page.');
                    window.location.reload();
                } else {
                    alert('Unable to process your request \n Please try again after sometime.');
                }
            }
        });
    }
}
