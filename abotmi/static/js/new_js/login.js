var csrf_token = $("#id_csrf_token").val();
var token = csrf_token;
var email = $('#email');
var is_direct_signup_valid = '';
var a_login_button = $("a[name=login_a]");
var a_signup_button = $("a[name=signup_a]");
var direct_signup_button = $("#email_signup_button");
var login_submit = $("#login_button");
var fb_btn = $("#fb_button");
var google_btn = $("#google_sign_button");
var linkedin_btn = $("#linkedin_button");
var upwrdz_soc_perm_ok = $("[name='upwrdz_soc_perm_ok']");
var why_to_signup_link = $("[name='why_to_signup']");
var user_role = $("[name='user_type']");
var is_mobile_verified = true;
var is_email_verified = true;
var is_advisor_clicked_google = true;
var profile_id;
var search_adv_btn = $("#discover_more");

$("#id_country_type").val(ad_chk_country);

// function for load the bootstrap modal
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: 'static'
    });
}

// attaching intelTelInput plugin to mobile input field
$(document).ready(function() {
    $("#mobile").intlTelInput({
        nationalMode: false,
        initialCountry: user_agent_country,
        separateDialCode: true,
    });
    $("#mobile").intlTelInput("setNumber", "+91");
});

// attaching click function to load Login Modal
a_login_button.click(function(){
    load_login_recaptcha();
    // to close guest signup modal
    $('.modal').on('show.bs.modal', function (e) {
        $('.modal').modal('hide');
    });
    $("#id_login_tab").css('display', 'block');
    $("#id_signup_tab").css('display', 'none');
    // checking Guest modal is present or not using id
    // to hide login/signup tabs for guest login modal
    if($('#id_guest_login_tab').length){
        $("#id_signup_tab").css('display', 'none');
        $("#id_login_tab").css('display', 'none');
        $('.close-icon').css('top', 0);
    }
    $(".carousel").carousel('pause');
    $("#signup-login-modal").modal('show');
    $("#id_login_tab").click();
});

// attaching click function to load Signup Modal
a_signup_button.click(function (e) {
    if (this.id == 'discover_more' || $(this).attr('role_check') == 'investor'){
        $("#investor_btn").prop('checked', true);
        show_or_hide_pwd_block();
    }else{
        $("#advisor_btn").prop('checked', true);
        // $(".sign-up-social-icons").removeClass('hide');
        show_or_hide_pwd_block();
    }
    load_email_signup_recaptcha();
    $("#id_signup_tab").css('display', 'block');
    $("#id_login_tab").css('display', 'none');
    $('#transform-advisor-id').modal('hide');
    $('#reput-manage-id').modal('hide');
    $('#bussiness-manage-id').modal('hide');
    $('#get_advice_free').modal('hide');    
    $(".carousel").carousel('pause');
    show_bootstrap_modal('#signup-login-modal');
    $("#id_signup_tab").click();
});

// function to load login_user function on click of Sign In button of login modal form
login_submit.click(function(){
    login_user();
});

// Action -> show forgot screen and hide login screen
function show_forgot_screen() {
    load_forgot_pwd_recaptcha();
    $('.additional_info').toggle();
}

// Validating the required fields while keyup/keydown
$("#first_name, #mobile, #email, #username, #password, #resend_email, #id_ad_chk_loc, #id_country_type").on('change keyup keydown paste',function() {
    var help_id = $('#'+this.id).closest(".form-group").find('.help-block')[0].id;
    var field_name = '';
    if (this.id == 'first_name'){
        field_name = 'First Name';
    }else if(this.id == 'mobile'){
        field_name = 'Mobile Number';
    }else if(this.id == 'email' || this.id == 'username'){
        field_name = 'Email';
    }else if(this.id == 'password'){
        field_name = 'Password';
    }else if(this.id == 'id_ad_chk_loc'){
        field_name = 'City';
    }else if(this.id == 'id_country_type'){
        field_name = 'Country';
    }
    var is_valid = validate_field_onkeypress(this.id, help_id, field_name);
    if (this.id == 'email' && is_valid!=1){
        is_direct_signup_valid = true;
    }
});

// Validating the signup form
function validate_member_input(){
    var is_city = validate_field_onkeypress('id_ad_chk_loc', 'id_ad_chk_loc_error_msg', 'City');
    var is_country = validate_field_onkeypress('id_country_type', 'id_country_type_error_msg', 'Country');
    var is_name = validate_field_onkeypress('id_ad_chk_f_name', 'id_ad_chk_f_name_error_msg', 'Advisor name');
    var is_email = validate_field_onkeypress('id_ad_chk_email', 'id_ad_chk_email_error_msg', 'Email');
    if (is_country == 0 || is_city == 0){
        a_signup_button.click();
        $("#investor_btn").prop('checked', true);
        show_or_hide_pwd_block();
    }else{ 
        return false;
    }
}

//Written jquery for hiding and showing the instruction block when user entered invalid password
$("#password_set").keypress(function(){
    is_password = validate_field_onkeypress('password_set', 'error_password', 'Password');
    if (is_password != 0){
        document.getElementById("my_pop").style.display = "inline";
    }else{
        document.getElementById("my_pop").style.display = "none";
    }
});

// Validating the signup form
function validate_direct_signup_form(){
    var is_password = 0;
    var is_signup_recaptcha = validate_recptcha(email_signup_recaptcha, 'help_signup_recpatcha');
    var is_mobile = validate_field_onkeypress('mobile', 'errormobile', 'Mobile Number');
    var is_email = validate_field_onkeypress('email', 'erroremail', 'Email');
    if ($('input[name="role_chk"]:checked').val() == 'advisor'){
        is_password = validate_field_onkeypress('password_set', 'error_password', 'Password');
    }
    var is_confirm_password = validate_field_onkeypress('password_set_confirm', 'error_confirm_password', 'Confirm Password');
    var is_last_name = validate_field_onkeypress('last_name', 'error_last_name', 'Last Name');
    var is_first_name = validate_field_onkeypress('first_name', 'errorfirst_name', 'First Name');
    if(is_first_name !=0 || is_email != 0 || is_mobile != 0 || is_password != 0 || is_confirm_password != 0 ||  is_last_name != 0 || is_signup_recaptcha != true){
            return false;
    }else{
        return true;
    }
}

// validating the Login form
function validate_login() {
    var is_login_recaptcha = validate_recptcha(login_recaptcha, 'help_login_recpatcha');
    var is_password = validate_field_onkeypress('password', 'help_password', 'Password');
    var is_username = validate_field_onkeypress('username', 'help_username', 'Email');
    if(is_username !=0 || is_password != 0 || is_login_recaptcha != true){
            return false;
    }else{
        return true;
    }
}

// validating the Forgot Password form
function validate_forgot_password(){
    var is_resend_email = validate_field_onkeypress('resend_email', 'help_resend_mail', 'Email');
    var is_forgot_recaptcha = validate_recptcha(forgot_password_recaptcha, 'help_forgot_recpatcha');
    if(is_resend_email != 0 || is_forgot_recaptcha != true){
            return false;
    }else{
        return true;
    }
}

// function for user login
function login_user(){
    var token = csrf_token;
    var is_valid = validate_login();
    if (is_valid){
        $.ajax({
            url: '/login/user_login/',
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken",token);
            },
            data: {
                username: $('#login_form').find('#username').val(),
                password: $('#login_form').find('#password').val(),
                next: next_url
            },
            success: function(response){
                if(response.status == 'true'){
                    $('#error_msg').html('');
                    var page_type = $("[name='page_type']").val();
                    if (page_type == 'identity'){
                        window.location.href = profile_link;
                    } else if (page_type == 'reputation'){
                        window.location.href = repute_link;
                    }else{
                        window.location.href = response.next;
                    }
                }
                else if(response.messages == 'not advisor') {
                    $("#northfacing_page_modal").modal('show');
                }
                else {
                    $('#error_msg').html('Invalid User Email ID / Password');
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                if (xhr.status == 403) {
                    show_alert(
                        'error',
                        'signup-login-modal',
                        '<p>You might have already loggedin <br /> Please Wait we are refreshing your page.<p>',
                        'reload:true'
                    );
                }else{
                    show_alert(
                        'error',
                        'signup-login-modal',
                        '<p>Unable to process your request \n Please try again after sometime.<p>'
                    );
                }
            }
        });
    }
}

// function will call on click of Sign up with Email button in signup form
direct_signup_button.click(function(){
    login_type = 'direct';
    var email_val = $('#signup_email_form').find('#email').val();
    var mobile_val = $('#signup_email_form').find('#mobile').val();
    var first_name = $('#signup_email_form').find('#first_name').val();
    if(validate_direct_signup_form()){
        ////check_user_exist
        if ($('input[name="role_chk"]:checked').val() != 'investor'){
            var check_email_result = check_email(email_val);
            check_email_result.complete(function (e, xhr, settings) {
                var status = e.status;
                if (status == 204) {
                    send_signup_otp(email_val,mobile_val,first_name);
                    $("a[name='resend_email_otp']").removeAttr('request_type');
                }else{
                    $("#user_already_exist_msg")
                        .fadeIn()
                        .fadeOut(5000, 'swing');
                }
            });
        }else{
            send_signup_otp(email_val, mobile_val, first_name);
            $("a[name='resend_email_otp']").removeAttr('request_type');
        }
    }
});

// Sending OTP 
function send_signup_otp(email, mobile, name){
    $.ajax({
        url: '/login/signup_otp/',
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data: {
            first_name: name,
            email: email,
            mobile: mobile
        },
        success: function (e, xhr, settings) {
            if (settings.status == 200) {
                $("#signup-login-modal").modal('hide');
                if ((e.ip_country != "IN" && login_type == 'direct') || (login_type != 'direct')) {
                    $("#mobile_otp_block_div").addClass('hide');
                } else {
                    $("#mobile_otp_block_div").removeClass('hide');
                    $("#email_otp_block").removeClass('hide');
                }
                $("#signup_otp_model").modal({
                    'show': true,
                    'keyboard': false,
                    'backdrop': 'static'
                });
            } else {
                show_alert(
                    'error',
                    'signup-login-modal',
                    '<p>Unable to send OTP <br /> Please try again.<p>'
                );
            }
        },
        error: function (response) {
            show_alert(
                'error',
                'signup-login-modal',
                '<p>Unable to send OTP <br /> Please try again.<p>'
            );
        }
    });
}

// function for sending resend link to Email Ids
function resend_password_link() {
    var token = csrf_token;
    resend_email = $('#signup_email_form').find('#email').val();
    if (resend_email) {
        $.ajax({
            url: '/signup/reset/',
            type: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                resend_email: resend_email,
                resend_link: 'resend_link'
            },
            success: function (response) {
                if (response.status == 200) {
                    if (!response.success) {
                        $("#success_modal_content").html('');
                        $("#success_modal_content").html('We have been sent you an email. please check your email.');
                        $("#success_modal_content")
                            .fadeIn()
                            .fadeOut(5000, 'swing');
                    } else {
                        $('#help_resend_mail').html("Resend mail has been failed.");
                    }
                }
            },
            error: function (response) {
                alert('Unable to send forgot password link.');
                show_alert(
                    'error',
                    'signup-login-modal',
                    '<p>Unable to send Forgot Password link <br /> Please try again.<p>'
                );
            }
        });
    } else {
        show_alert(
            'error',
            'signup-login-modal',
            '<p>Unable to send Forgot Password link <br /> Please try again.<p>'
        );
    }
}

// function for sending resetpassword link to forgot password Email Ids
function forgot_user_pwd(){
    var token = csrf_token;
    if(validate_forgot_password()){
        $.ajax({
            url: '/signup/reset/',
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken",token);
            },
            data: {
                resend_email: $('#forgot_pwd_form').find('#resend_email').val()
            },
            success: function(response){
                if(response.status == 200){
                    if(!response.success){
                        $("#help_resend_mail").html('');
                        $('.input').val('');
                        $('#signup-login-modal').modal('hide');
                        $("#success_alert_modal_content").html('');
                        $("#success_alert_modal_content").html('We have sent you an email with an instructions on how to reset your password <br/> please check your email.');
                         document.getElementById('confirm_btn').innerHTML = 'OK';
                        $("#success_alert_modal").modal('show');
                    }else if (response.success == 'not_advisor') {
                        $('#help_resend_mail').html("You are not an Advisor");
                    }else{
                        $('#help_resend_mail').html("You are not a Registered User");
                    }
                }else if(response.status == 204){
                    $('.input').val('');
                    $('#help_resend_mail').html('User Does Not Exist');
                }
            },
            error: function(response){
                show_alert(
                    'error',
                    'signup-login-modal',
                    '<p>Unable to send Forgot Password link <br /> Please try again.<p>'
                );
            }
        });
    }
}


// =================================================================================== //
//  Below function for Social Media signup. to work below scripts remove comment block
//  tags in login html
// =================================================================================== //
// functions for showing Social Media permisson modal on click of Facebook/Google/Linkedin button
fb_btn.on('click', function (e) {
    if ($("[name='user_type']").val() == 'member') {
        upwrdz_soc_perm_ok.attr("onclick", "facebookMemberLogin('signup_or_login', 'member');");
    } else {
        // facebookLogin('signup_or_login', 'advisor');
        upwrdz_soc_perm_ok.attr("onclick", "facebookLogin('', 'advisor');");
    }
    show_upwrdz_permission_modal('#signup-login-modal');
});


// function for show the Social Media Permisson modal
function show_upwrdz_permission_modal(hide_modal_id) {
    $(hide_modal_id).modal('hide');
    $('#upwrdz_soc_perm_modal').modal('show');
}

// enable the socia media button after accepting the our conditions in social media permisson modal
function enabled_ok(){
    if($('#check_permisson').prop('checked')) {
        $('#social_media_btn').prop('disabled', false);
    }else{
        $('#social_media_btn').prop('disabled', true);
    }
}
// ===================================================================================== //

function set_user_role(user_role_type){
    $.ajax({
        type: "POST",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: '/login/set_user_role/',
        data:{
            user_role: user_role_type
        },
        success: function(response){
            $("#id_user_question").modal('hide');
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if(xhr.status == 403){
                alert('You might have already loggedin \n Please Wait we are refreshing your page.');
                window.location.reload();
            }else{
                alert('Unable to process your request \n Please try again after sometime.');
            }
        }
    });
}

// *********** OTP Scripts ***************
// function for sending OTP to mobile
function resend_otp_mobie_email(mode) {
    var email = $('#signup_email_form').find('#email').val();
    var mobile = $('#signup_email_form').find('#mobile').val();
    var first_name = $('#signup_email_form').find('#first_name').val();
    var mode = mode;
    var request_from = $("a[name='resend_email_otp']").attr('request_type');
    if(request_from){
        mobile = '';
        if(request_from == 'facebook'){
            email = fb_respnce_data.email;
            first_name = fb_respnce_data.first_name;
        }else if(request_from == 'linkedin'){
            email = ln_email;
            first_name = ln_first_name;
        }
    }
    
    $.ajax({
        method: 'POST',
        url: '/login/resend_email_mobile_otps/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: { 
            'email' : email, 
            'mobile' : mobile, 
            'mode' : mode, 
            'name' : first_name
        },
        success: function (e, xhr, settings) {
            if (settings.responseJSON.status == 200) {
                if(settings.responseJSON.mode == 'mobile'){
                    $("#mobile_otp_success_text_msg")
                        .fadeIn()
                        .fadeOut(5000, 'swing');
                    is_mobile_verified = false;
                }else{
                    $("#email_otp_success_text_msg")
                        .fadeIn()
                        .fadeOut(5000, 'swing');
                    is_email_verified = false;
                }
                $('#id_submit_investor_otp_button').removeAttr('disabled');
                $('#id_submit_investor_otp_button').removeClass('upwrdz-button-verify');
            }
        }
    });
}

// function for going back from OTP modal to Signup Modal
function go_back(){
    $("#signup-login-modal").modal('show');
    $("#otp_verified_message_model").modal('hide');

}

// function for load OTP modal  
function show_verify_otp_modal(link) {
    $("#signup-login-modal").modal('hide');
    $("#id_submit_investor_otp")
        .removeAttr('onclick')
        .bind('click', [profile_id, link], submit_otp);
    $("#otp_verified_message_model").modal({
        'show': true,
        'keyboard': false,
        'backdrop': 'static'
    });

    $("#submit_otp_email_id")
        .removeAttr('onclick')
        .bind('click', ['email_val'],verify_email_otp);

    $("#submit_otp_mobile_id")
        .removeAttr('onclick')
        .bind('click', ['mobile_val'], verify_mobile_otp);

    $("#mobile_otp_resend_id")
        .removeAttr('onclick')
        .bind('click', [profile_id, 'mobile'], resend_mobile_otp);
    $("#email_otp_resend_id")
        .removeAttr('onclick')
        .bind('click', [profile_id, 'email'], resend_mobile_otp);
    
    $("#id_back_btn")
        .removeAttr('onclick')
        .bind('click', go_back);
}

// Validate the mobile otp
$("#mobile_otp_id").on('keyup keypress change input', function (e) {
    if (validate_field_onkeypress(this.id, 'help_text_mobile_otp_id', 'Mobile OTP') == 0) {
        if ($(this).val().length == 6) {
            $('#submit_otp_mobile_id').prop('disabled', false);
            $('#submit_otp_mobile_id').removeClass('upwrdz-button-verify');
        } else {
        $('#submit_otp_mobile_id').prop('disabled', true);
        }
    }
});

// validate the email otp
$("#email_otp_id").on('keyup keypress change input', function(e){
    if (validate_field_onkeypress(this.id, 'help_text_email_otp_id', 'Email OTP') == 0){
        if($(this).val().length == 6){
            $('#submit_otp_email_id').removeAttr('disabled');
            $('#submit_otp_email_id').removeClass('upwrdz-button-verify');
        }else{
            $('#submit_otp_email_id').prop('disabled', true);
        }
    }
});

var is_email_verified = false;
var is_mobile_verified = false;

// Cheking NULL validatin for OTP form
function validate_mobile_otp(){
    var validate_mob_otp = 0;
    validate_mob_otp = validate_field_onkeypress(
            'mobile_otp_id', 'help_text_mobile_otp_id', ' Mobile OTP');
    if (ip_region =="IN" && validate_mob_otp != 0) {
        return false;
    } else {
        return true;
    }
}

function verify_mobile_otp(){
    var otp_form_valid_result = validate_mobile_otp();
    var mobile_val = $('#signup_email_form').find('#mobile').val();
    if(otp_form_valid_result){
        $("#help_text_mobile_otp_id").html('');
        $.ajax({
            method: 'POST',
            url: '/login/validate_otp/',
            beforeSend: setHeader,
            data:{
                'mobile_otp': $("#mobile_otp_id").val(),
                'first_name': $("#first_name").val(),
                'signup_otp': 'signup_otp',
                'mobile' : mobile_val
            },
            success: function (e, xhr, settings) {
                if (settings.status == 200) {
                    if (e.mob_verf_stat == true) {
                        is_mobile_verified = true;
                    }else{
                        $("#help_text_mobile_otp_id").html('Please Enter Valid OTP');
                    }
                    enable_otp_submit();
                }else{
                    $("#help_text_mobile_otp_id").html('Please Enter Valid OTP');
                }
            },
            error: function(response){
                alert('Unable to validate the Mobile OTP. \n Please try again after sometime');
            }
        });
    }else{
        return false;
    }
}


// Cheking NULL validatin for OTP form
function validate_email_otp(){
    var validate_email_otp = 0;
    validate_email_otp = validate_field_onkeypress(
            'email_otp_id', 'help_text_email_otp_id', ' Email OTP');
    if (validate_email_otp != 0 ){
        return false;
    } else {
        return true;
    }
}
// Verifying the OTP is correct or not
function verify_email_otp(){
    var otp_form_valid_result = validate_email_otp();
    var email_val = $('#signup_email_form').find('#email').val();
    if(otp_form_valid_result){
        $("#help_text_email_otp_id").html('');
        $.ajax({
            method: 'POST',
            url: '/login/validate_otp/',
            beforeSend: setHeader,
            data:{
                'email_otp': $("#email_otp_id").val(),
                'first_name': $("#first_name").val(),
                'signup_otp': 'signup_otp',
                'email' : email_val
            },
            success: function (e, xhr, settings) {
                if (settings.status == 200) {
                    if(e.email_verf_stat == true){
                        is_email_verified = true;
                        document.getElementById("email_otp_resend_id").style.display="none";
                        document.getElementById("submit_otp_email_id").style.display="none";
                    }else{
                        $("#help_text_email_otp_id").html('Please enter valid OTP');
                    }
                    enable_otp_submit();
                }else{
                    $("#help_text_email_otp_id").html('Please enter valid OTP');
                }
            },
            error: function(response){
                alert('Unable to Validate Email OTP. \n Please try agian after sometime');
            }
        });
    }else{
        return false;
    }
}

// Enable the otp submit button
function enable_otp_submit(){
    if (user_agent_country != 'IN' || login_type == 'facebook' || login_type == 'linkedin') {
        if(is_email_verified){
            $('#email_otp_verify_btn_div').addClass('hide');
            $('#email_otp_verified_id').removeClass('hide');                    document.getElementById("id_submit_investor_otp_button").style.display="block";
            $('#id_submit_investor_otp_button').removeAttr('disabled');
            $('#id_submit_investor_otp_button').removeClass('upwrdz-button-verify');
            
            // $('#back_button').addClass('hide');
        }
    }
    if(user_agent_country == 'IN'){
        if(is_mobile_verified && is_email_verified){
            $('#mobile_otp_verify_btn_div').addClass('hide');
            $('#mobile_otp_verified_div').removeClass('hide');
            $('#email_otp_verified_id').removeClass('hide');                    document.getElementById("id_submit_investor_otp_button").style.display="block";
            $('#id_submit_investor_otp_button').removeAttr('disabled');
            $('#id_submit_investor_otp_button').removeClass('upwrdz-button-verify');
        }
    }
}

// function for submitting the OTP
function submit_otp(params){
    $('#help_text_id_otp').html('');
    var id = params.data[0];
    var link = params.data[1];
    // if ((settings.status == 200 && e.mob_verf_stat && ip_region == "IN" && e.email_verf_stat) || (ip_region!= "IN" && settings.status == 200 && e.email_verf_stat)) {
    // if ((ip_region == "IN")) {
            $.ajax({
            method: 'POST',
            url:'/login/verify_otp_and_login/',
            beforeSend: setHeader,
            data:{
                'email_otp': $("#id_email_otp").val(),
                'mobile_otp': $("#id_mobile_otp").val(),
                'profile_id': id
            },
            success: function (e, xhr, settings){
                if(settings.status == 200){
                    if(link){
                        window.location.href=link;
                    }
                    else if ((e.is_mob_verf && e.is_email_verf && ip_region == "IN") || (e.is_email_verf && ip_region != "IN")){
                        window.location.href = '/';
                    }
                }else{
                    alert('Unable to process your request \n Please try again after some time');
                }
            },
            error: function(response){
                alert('Unable to process your request right now. \n Please try again after some time');
            }
        });
}

$("[name='role_chk']").on('change', function (e) {
    show_or_hide_pwd_block();
});

function show_or_hide_pwd_block(){
    if ($('input[name="role_chk"]:checked').val() == 'investor') {
        $("#password_block_div").addClass('hide');
        $("#password_set").val('');
    } else {
        $("#password_block_div").removeClass('hide');
        $("#password_set").val('');
    }
}


function submit_otp_signup(){
    if(login_type == 'facebook'){
        $("#signup_otp_model").modal('hide');
        facebook_social_signup();
    }else if(login_type == 'linkedin'){
        $("#signup_otp_model").modal('hide');
        linkedin_soc_signup();
    }
    else{
        directSignupWithEmail();
    }
}

// Signup with Email(Direct signup)
function directSignupWithEmail() {
    var referral = ref;
    $.ajax({
        url: '/login/email_signup/',
        type: 'POST',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            ref_link: referral,
            user_selected_role: $('input[name="role_chk"]:checked').val(),
            first_name: $('#signup_email_form').find('#first_name').val(),
            last_name: $('#signup_email_form').find('#last_name').val(),
            email: $('#signup_email_form').find('#email').val(),
            mobile: $('#signup_email_form').find('#mobile').val(),
            password: $('#signup_email_form').find('#password_set').val(),
            ad_chk_loc: $("#id_ad_chk_loc").val(),
            ad_chk_country: $("[name='country_type']").val(),
            ad_chk_name: $("#id_ad_chk_f_name").val()
        },
        complete: function (e, xhr, settings) {
            var response = e.responseJSON;
            if (e.status == 201) {
                if (response.user_selected_role == 'advisor') {
                    if (next_url){
                        window.location.href = $('#next_url').val();
                    }else{
                        window.location.href = '/advisor_check/get_advisor_card/';
                    }
                } else {
                    if (next_url) {
                        window.location.href = $('#next_url').val();
                    }else{
                        window.location.href = '/member/';
                    }
                }
            } else if (e.status == 200) {
                if (response.user_selected_role == 'advisor') {
                    alert('User already exists');
                } else {
                    if (next_url) {
                        window.location.href = $('#next_url').val();
                    }else{
                        window.location.href = '/member/';
                    }
                }
            } else {
                alert('Unable to process your request \n Please try again after sometime');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if (xhr.status == 403) {
                alert('You might have already loggedin \n Please Wait we are refreshing your page.');
                window.location.reload();
            } else {
                alert('Unable to do Signup. Please try after some time.');
            }
        }
    });
}

// Showing popover for password help content
$('[rel="popover"]').popover({
    container: 'body',
    html: true,
    content: function () {
        var clone = $($(this).data('popover-content')).clone(true).removeClass('hide');
        return clone;
    }
}).click(function (e) {
    e.preventDefault();
});

// show/hide the password
$('.pwd-add-on').on('click', function (e) {
    var icon;
    if ($("#password").attr('type') == 'password') {
        icon = '<i class="fa fa-eye-slash"></i>';
        $('#password').attr('type', 'text');
    } else {
        icon = '<i class="fa fa-eye"></i>';
        $('#password').attr('type', 'password');
    }
    $(this).html(icon);
});

$('.pwd-sign-on').on('click', function (e) {
    var icon;
    if ($("#password_set").attr('type') == 'password') {
        icon = '<i class="fa fa-eye-slash"></i>';
        $('#password_set').attr('type', 'text');
    } else {
        icon = '<i class="fa fa-eye"></i>';
        $('#password_set').attr('type', 'password');
    }
    $(this).html(icon);
});