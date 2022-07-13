var csrf_token = $("#id_csrf_token").val();
var from_state = "";
var next_navigation_url = $('#next_url');
var linkedin_btn = $("[name='linkedin_button']");


linkedin_btn.on('click', function(e){
    var url_prams = {
        'user_selected_role': $('input[name="role_chk"]:checked').val(),
        'ad_chk_loc': $("#id_ad_chk_loc").val(),
        'ad_chk_country': $("[name='country_type']").val(),
        'ad_chk_reg': $("#id_ad_chk_type").val(),
        'ad_chk_name': $("#id_ad_chk_f_name").val(),
        'next_url': $("#next_url").val()
    };
    window.location.href = '/login/linkedin?'+$.param(url_prams);
});

$(document).ready(function(e){
    if (ln_res != 'ln_error') {
        if (ln_email && (ln_first_name || ln_last_name)) {
            var check_email_result = check_user_exist(ln_email);
            login_type = 'linkedin';
            if(ln_user_selected_role != 'investor'){
                check_email_result.complete(function (e, xhr, settings) {
                    var status = e.status;
                    if (status == 204) {
                        send_signup_otp(ln_email, '', ln_first_name);
                        $("a[name='resend_email_otp']").attr('request_type', 'linkedin');
                    } else {
                        linkedin_soc_signup();
                    }
                });
            }else{
                send_signup_otp(ln_email, '', ln_first_name);
                $("a[name='resend_email_otp']").attr('request_type', 'linkedin');
            }
        }
    }
    else{
        if (ln_res == 'ln_error'){
            alert('Unable to get the response from Linkedin \n Please try again with different social media or check after some time');
        }
    }
});


function linkedin_soc_signup(){
    $.ajax({
        type: "POST",
        url: "/login/social_media_login/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            user_name: ln_email,
            first_name: ln_first_name,
            last_name: ln_last_name,
            email: ln_email,
            source_media: 'linkedin',
            next_url: $('#next_url').val(),
            ref_link: ref,
            // Advisor check search data
            ad_chk_loc: $("#id_ad_chk_loc").val(),
            ad_chk_country: $("[name='country_type']").val(),
            ad_chk_name: $("#id_ad_chk_f_name").val(),
            // user selected role
            user_selected_role: ln_user_selected_role
            
        },
        success: function (response) {
            if (response.log_usr_type == 'company_user') {
                window.location = $('#id_company_url').val();
            }
            if (response.account_type == "deactivated") {
                alert('your account is not active call customer care');
            } else {
                if (ln_user_selected_role == 'advisor') {
                    if (ln_next_url) {
                        window.location.href = $('#next_url').val();
                    } else {
                        window.location.href = '/';
                    }
                } else {
                    if (ln_next_url) {
                        window.location.href = $('#next_url').val();
                    } else {
                        window.location.href = '/';
                    }
                }
            }
        }
    });
}