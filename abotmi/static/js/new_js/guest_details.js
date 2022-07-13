var csrf_token = $("#id_csrf_token").val();
var fb_member_btn = $("#fb_member_button");
var google_member_btn = $("#google_sign_member_button");
var linkedin_member_btn = $("#linkedin_member_button");
var upwrdz_soc_perm_ok = $("[name='upwrdz_soc_perm_ok']");
var hidden_page_type = $("input[name='page_type']");

// Attaching Country code plugin to mobile field
$(document).ready(function() {
    $("#guest_mobile").intlTelInput({
        nationalMode: false,
        initialCountry: "auto",
        separateDialCode: true,
        geoIpLookup: function (callback) {
            $.get('https://ipinfo.io', function () {}, "jsonp").always(function (resp) {
                var countryCode = (resp && resp.country) ? resp.country : "";
                callback(countryCode);
            });
        },
    });
});

// commented for temperorly
// $(document).ready(function(){
//     if(title){ document.getElementById('id_back_btn').style.visibility = 'visible';
//     } else { document.getElementById('id_back_btn').style.visibility = 'hidden';}
// })

// Showing Guest/Member signup Modal
function show_modal(page_type) {
    $('#identity').modal('show');
    $("#id_submit_guest").removeAttr('onclick');
    member_recaptcha();
    if(page_type == 'identity'){
        hidden_page_type.val('identity');
        $("#id_submit_guest").attr('onclick', 'guest_details("identity")');
    }else{
        hidden_page_type.val('reputation');
        $("#id_submit_guest").attr('onclick', 'guest_details("repute")');
    }
}

// Validating the Guest form on keyup/keydown
$("#guest_name, #guest_mobile, #guest_email").on('keyup keydown',function() {
    var help_id = $('#'+this.id).closest(".form-group").find('.help-block')[0].id;
    var field_name = '';
    if (this.id == 'guest_name'){
        field_name = 'Name';
    }else if(this.id == 'guest_mobile'){
        field_name = 'Mobile Number';
    }else if(this.id == 'guest_email'){
        field_name = 'Email';
    }
    validate_field_onkeypress(this.id, help_id, field_name);
});

// Validating the Guest form
function validate_guest_form(){
    var is_member_login_recaptcha = validate_recptcha(member_login_recaptcha, 'help_member_login_recaptcha');
    var is_mobile = validate_field_onkeypress('guest_mobile', 'help_guest_mobile', 'Mobile Number');
    var is_email = validate_field_onkeypress('guest_email', 'help_guest_email', 'Email');
    var is_first_name = validate_field_onkeypress('guest_name', 'help_guest_name', 'Name');
    if(is_first_name !=0
        || is_email != 0
        || is_mobile != 0
        || is_member_login_recaptcha!= true){
            return false;
    }else{
        return true;
    }
}

// Submitting Guest form for signup and Loading OTP form
function guest_details(page_type=undefined){
    var validation_result = validate_guest_form();
    if (validation_result){
        $.ajax({
            type: "POST", 
            url: "/login/email_signup/", 
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                'first_name' : $("#guest_name").val(),
                'email' : $("#guest_email").val(),
                'mobile': get_mobile_no("#guest_mobile"),
                'user_type': 'member',
                'social_auth_ses': 'False'
            },
            complete: function(e, xhr, settings){
                var response = JSON.parse(e.responseText);
                var page_link = '';
                if (e.status == 201 || e.status == 200) {
                    if (page_type == 'identity'){
                        page_link = profile_link;
                    }else if(page_type == 'repute'){
                        page_link = repute_link;
                    }
                    if (page_link && response.is_member){
                        $("#identity").modal('hide');
                        profile_id = response.profile_id;
                        show_verify_otp_modal(page_link);
                    } 
                    else { $('#help_guest_email').html("You are a Registered User.");
                           $('#guest_email').val('');}
                }
                else if(e.status == 500){
                    alert("Try after some time");
                }
            },
            error: function(response){
                alert('Unable to Process your request \n Please Try again after some time');
            }
        });
    }
}

// Loading Guest modal on click of back button in OTP modal
$('body').find("#otp_verified_message_model a").on('click', function(e){
    $("#otp_verified_message_model").modal('hide');
    show_bootstrap_modal('#identity');
});

// attaching facebook login function to social media permission modal
fb_member_btn.on('click', function(e){
    upwrdz_soc_perm_ok.attr("onclick", "facebookLogin('signup_or_login', 'member');");
    show_upwrdz_permission_modal('#identity');
});

// attaching facebook login function to social media permission modal
google_member_btn.on('click', function(e) {
    is_advisor_clicked_google = false;
    upwrdz_soc_perm_ok.attr("onclick", "$('#google_btn').click();");
    show_upwrdz_permission_modal('#identity');
});

// attaching facebook login function to social media permission modal
linkedin_member_btn.on('click', function(e) {
    upwrdz_soc_perm_ok.attr("onclick", "onLinkedInLoad('signup_or_login', 'member');");
    show_upwrdz_permission_modal('#identity');
});