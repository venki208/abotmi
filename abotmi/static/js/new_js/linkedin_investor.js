var csrf_token = $("#id_csrf_token").val();
var from_state = "";
var linkedin_user_type = '';

// Setup an event listener to make an API call once auth is complete
function memberOnLinkedInLoad(from_state, user_type=undefined) {
    localStorage.removeItem('from_state_for_ln');
    localStorage.setItem('from_state_for_ln', from_state);
    from_state = from_state;
    linkedin_user_type = user_type;
    IN.UI.Authorize().place();
    IN.Event.on(IN, "auth", memberOnLinkedInAuth);
}

// Use the API call wrapper to request the member's basic profile data
function memberOnLinkedInAuth() {
    IN.API.Profile("me")
    .fields("firstName", "lastName", "industry", "location:(name)", "picture-url", "headline", "summary", "num-connections", "public-profile-url", "distance", "positions", "email-address", "educations","date-of-birth")
    .result(memberdisplayProfiles)
    .error(memberdisplayProfilesErrors);
}

// show the otp modal
function show_verify_otp_modal_social_signup(profile_id,link){
    $("#id_submit_otp_social")
        .removeAttr('onclick')
        .attr('onclick', "submit_otp_social("+"'"+profile_id+"',"+"'"+link+"')");
    $("#investor_social_otp_verified_message_model").modal({
        'show': true,
        'keyboard': false,
        'backdrop': 'static'
    });
    $("#id_submit_otp_investor_email")
        .removeAttr('onclick')
        .bind('click', [profile_id, 'email'], verify_otp_data_social);

    $('#id_email_otp_resend_social').unbind();
    $("#id_email_otp_resend_social")
        .removeAttr('onclick')
        .attr('onclick', "resend_investor_otp("+"'"+profile_id+"',"+"'email')");
    $("#id_back_btn")
        .removeAttr('onclick')
        .attr('onclick', go_back);
}

$(document).ready(function () {
    $('#id_email_otp_social').bind('paste', function (e) {
        var mobiles = e.originalEvent.clipboardData.getData('Text').trim();
        if (mobiles.length) {
            $('#id_submit_otp_investor_email').prop('disabled', false);
            $('#id_submit_otp_investor_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_otp_investor_email').prop('disabled', true);
        }
    });
});

function validate_social_investor_email_otp() {
    var emails = $('#id_email_otp_social').val().trim();
    if (user_agent_country == "IN") {
        if (emails.length>0) {
            $('#id_submit_otp_investor_email').prop('disabled', false);
            $('#id_submit_otp_investor_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_otp_investor_email').prop('disabled', true);
        }
    } else if (user_agent_country != "IN") {
        if (emails.length>0) {
            $('#id_submit_otp_investor_email').prop('disabled', false);
            $('#id_submit_otp_investor_email').removeClass('upwrdz-button-verify');
        } else {
            $('#id_submit_otp_investor_email').prop('disabled', true);
        }
    }
}

// Cheking NULL validatin for OTP form
function validate_otp_form_social() {
    var validate_email_otp = 0;
    validate_email_otp = validate_field_onkeypress(
        'id_email_otp_social', 'help_text_id_email_otp_social', ' Email OTP');
    if (validate_email_otp != 0) {
        return false;
    } else {
        return true;
    }
}

// Verifying the OTP is correct or not
function verify_otp_data_social(params) {
    var id = params.data[0];
    var otp_form_valid_result = validate_otp_form_social();
    if (otp_form_valid_result) {
        return $.ajax({
            method: 'POST',
            url: '/login/validate_otp/',
            beforeSend: setHeader,
            data: {
                'email_otp': $("#id_email_otp_social").val(),
                'mobile_otp': $("#id_mobile_otp").val(),
                'profile_id': id
            },
            success: function (e, xhr, settings) {
                if (settings.status == 200) {
                    if (e.email_verf_stat == true) {
                        $('#social-email-otp-verify-btn-div').addClass('hide');
                        $('#social_email_otp_verified').removeClass('hide');
                        $('#id_submit_otp_social').prop('disabled', false);
                        $('#back_btn').prop('disabled', true);
                        $('#id_submit_otp_social').removeClass('upwrdz-button-verify');
                    }
                    else{
                        $("#help_text_id_email_otp_social").html('Please enter valid OTP');
                    }
                }
            }
        });
    } else {
        return false;
    }
}

// resend otp for social media
function resend_investor_otp(id, mode){
    // var id = params.data[0];
    // var mode = params.data[1];
    $.ajax({
        method: 'POST',
        url: '/login/resend_otp/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: { 'profile_id': id, 'mode': mode },
        success: function (e, xhr, settings) {
            if (settings.status == 200) {
                $("#mobile_otp_success_text")
                    .fadeIn()
                    .fadeOut(5000, 'swing');
            }
        }
    });
}

//submit the otp and login 
function submit_otp_social(profile_id, link) {
    var id = profile_id;
    var link = link;
    //  verify_otp_result.success(function (e, xhr, settings) {
            // if ((settings.status == 200 && e.email_verf_stat) ) {
        // if (user_agent_country =="IN") {
            $.ajax({
                method: 'POST',
                url: '/login/verify_otp_and_login/',
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                    'email_otp': $("#id_email_otp_social").val(),
                    'mobile_otp': $("#id_mobile_otp").val(),
                    'profile_id': id
                },
                success: function (e, xhr, settings) {
                    if (e.is_email_verf) {
                        window.location.href = '/';
                    }
                    else {
                        alert('Unable to process your request \n Please try again after some time');
                    }
                }
            });
}
// Submitting the success data from Linkedin
function memberdisplayProfiles(profiles) {
    member = profiles.values[0];
    positions = "";
    summary = "";
    if(member.positions != undefined){
        if(member.positions.values != undefined){
            if(member.positions.values.length > 0){
                positions = member.positions.values;
  	            $.each(positions, function( index, value ) {
                    if(value.summary != undefined){
                        summary = value.summary;
                        return false;
                    }
                });
            }
        }
    }
    var token = csrf_token;
    var email = member.emailAddress;
    var headline = member.headline;
    from_state = localStorage.getItem('from_state_for_ln');
    if(from_state == "signup_or_login"||from_state=="social_auth"||from_state==""){
      var referral = "";
      $.ajax({
        type: "POST",
        url: "/login/investor_social_media_login/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token );
        },
        data: {
            user_name : email,
            first_name: member.firstName,
            last_name : member.lastName,
            email     : email,
            gender    : 'Male',
            birthday  : '1990-07-11',
            source_media : 'linkedin',
            next_url  : $('#next_url').val(),
            user_type : linkedin_user_type,
            ref_link  : referral,
            headline : headline,
            summary : summary, 
            social_auth: from_state,
            inv_chk_login: $("[name='get_advice_hidden']").val(),
            ad_chk_name: $("#id_ad_chk_f_name").val(),
            ad_chk_email: $("#id_ad_chk_email").val(),
            ad_chk_mob: $("#id_ad_chk_mobile").val(),
            ad_chk_loc: $("#id_ad_chk_loc").val(),
            ad_chk_country: $("[name='country_type']").val()
        },
        success:function(response) {
            $('#signup-login-modal').modal('hide');
            $('#upwrdz_soc_perm_modal').modal('hide');
            var page_type = $("input[name='page_type']").val();
            if (response.exist_user == "new_user") {
                memberShareContent();
            }
            $('#check_social_media_details').modal('hide');
            if ($("[name='user_type']").val() == "member" && !response.is_authenticated){
                show_verify_otp_modal_social_signup(response.profile_id, $('#next_url').val());
            }
            if(response == "deactivated"){
                alert('your account is not active call customer care');
            }
        }
      });
    }else{
        member_check_social_email_for_linkedin(email, headline, summary);
    }
}

// Checking Login email id and Linked in email id are same or not
function member_check_social_email_for_linkedin(email, headline, summary){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/reputation-index/check_social_email/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data : {
            email  : email
        },
        success:function(response) {
            var res_status = response.status;
            if(res_status){
                member_advisor_scoring_linedin(email, headline, summary);
            }else{
                alert('Please use same username for linkedin');
            }
        },error:function(response){
            alert('Unable process request. Please try after some time');
        }
    });
}

// Adding score for sharing Linkedin information 
function member_advisor_scoring_linedin(email, headline, summary){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/reputation-index/advisor-scoring-linkedin/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data : {
            email  : email,
            headLine : headline,
            summary : summary
        },
        success:function(response) {
            if(response.status){
                alert("Scoring submitted successfully");
            }else{
                alert(response.message);
            }
        }
    });
}

// Setting error message
function memberdisplayProfilesErrors(error) {
    profilesDiv = document.getElementById("fetch_data");
    profilesDiv.innerHTML = error.message;
}

// Sharing the UPWRDZ content to users Linkedin wall
function memberShareContent() {
          // Build the JSON payload containing the content to be shared
          var payload = {
            "comment": "Check out UPWRDZ.com",
            "content": {
              "title": "UPWRDZ",
              "description": "Grow by Creating Wealth for the Real Estate Investors",
              "submitted-url": "{% get_social_media 'LINKEDIN_SINGLE_URL' %}",
              "submitted-image-url": "{% get_social_media 'LINKEDIN_IMAGE_URL' %}"
          },
          "visibility": {
              "code": "anyone"
          }
      };

      IN.API.Raw("/people/~/shares?format=json")
      .method("POST")
      .body(JSON.stringify(payload))
      .result(onMemberSuccess)
      .error(onMemberError);
}

function onMemberSuccess(data) {
    var data = data;
}

function onMemberError(error) {
    var error = error;
}
