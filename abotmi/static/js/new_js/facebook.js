var csrf_token = $("#id_csrf_token").val();
var fb_respnce_data = fb_respnce_data;
var fb_token;

/**
 * @use: Login/Signup with Facebook
 * @param {String} (from_state) -> need to pass 'signup_or_login|member_login|social_auth'
 * @param {String} (user_type) - > need to pass 'advisor|member'
*/
function facebookLogin(from_state, user_type=undefined){
    FB.login(function(response) {
        if (response.status === 'connected') {
            fb_token = response.authResponse.accessToken;
            // for first time user it will ask permissions to log into our website.
            // checking required fields are checked are not in permission popup.
            FB.api('/me/permissions', function(response) {
                var declined = [];
                for (i = 0; i < response.data.length; i++) {
                    // checking unchecked fields in permission popup
                    if (response.data[i].status == 'declined') {
                        declined.push(response.data[i].permission);
                    }
                }
                // if email field is not checked in permission popup it will go basic login flow
                for(i=0; i<=declined.length; i++){
                    if(declined[i] == 'email'){
                        try {
                            if($('#signup-modal').data('bs.modal').isShown == true){
                                $('#signup-modal').modal('hide');
                                $("#check_fb_details").modal('show');
                            }
                        }
                        catch(err) {
                                $("#check_fb_details").modal('show');
                        }
                        return false;
                    }
                    else{
                        get_user_details(from_state, fb_token, user_type);
                    }
                }
            });
        } else if (response.status === 'not_authorized') {
            alert('you are not authorized');
        } else {
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
        }
    }, {
            // scope fields will show to ask permission for first time user in our website.
            scope: 'public_profile,email,user_birthday,user_likes,user_friends,user_location,user_hometown,read_custom_friendlists',
            force:true,
            auth_type:'rerequest'
        });
}

// FB share reiaglobal page with cover photo
function fb_share(user_type){
    FB.ui({
        method: 'share',
        display: 'popup',
        href: facebook_single_url,
    }, function(response){
        // // var page_type = $("input[name='page_type']").val();
        navigate_to_page(user_type);
    });
}
var from_state;
/**
 * @use: Getting user details from Facebook and Sending data to backend through ajax to 
 *      complete the signup/Login
 */
// var login_type;
function get_user_details(from_state, fb_token, user_type){
    $("#check_fb_details").modal('hide');
    login_type = 'facebook';
    FB.api('/me',{fields:'first_name,last_name,email,gender,birthday,verified'},
        function(response) {
            fb_respnce_data = response;
            from_state = from_state;
            user_type = user_type;
            if ($('input[name="role_chk"]:checked').val() != 'investor'){
                var check_email_result = check_user_exist(response.email);
                check_email_result.complete(function (e, xhr, settings) {
                    var status = e.status;
                    if (status == 204) {
                        send_signup_otp(response.email, '', response.first_name);
                        $("a[name='resend_email_otp']").attr('request_type', 'facebook');
                    }else{
                        facebook_social_signup();
                    }
                });
            }else{
                send_signup_otp(response.email, '', response.first_name);
                $("a[name='resend_email_otp']").attr('request_type', 'facebook');
            }
        });
}

function facebook_social_signup(){
    var myBD = fb_respnce_data.birthday;
    // Update Hidden inputs
    var birthday = "";
    if (typeof myBD != 'undefined'){
        var fb_date = fb_respnce_data.birthday;
        var fb_date_array = fb_date.split('/');
        birthday = fb_date_array[2]+"-"+fb_date_array[0]+"-"+fb_date_array[1];
    }
    var token = csrf_token;
    if (from_state == "signup_or_login" 
        || from_state == "member_login" 
        || from_state == "social_auth"
        || from_state == '')
    {
        var referral = "";
        $('#signup-login-modal').modal('hide');
        $.ajax({
            type: "POST",
            url: "/login/social_media_login/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data : {
                first_name : fb_respnce_data.first_name,
                last_name  : fb_respnce_data.last_name,
                email  : fb_respnce_data.email,
                birthday : birthday,
                gender : fb_respnce_data.gender,
                source_media : 'facebook',
                next_url : $('#next_url').val(),
                // user_type : user_type,
                ref_link : referral,
                token : fb_token,
                // Advisor check search data
                ad_chk_loc: $("#id_ad_chk_loc").val(),
                ad_chk_country: $("[name='country_type']").val(),
                ad_chk_name: $("#id_ad_chk_f_name").val(),
                // user selected role
                user_selected_role: $('input[name="role_chk"]:checked').val()
            },
            success:function(response) {
                if (response.log_usr_type == "user_exist") {
                    navigate_to_page(response.user_selected_role);
                } else if (response.log_usr_type == "new_user") {
                    $('#check_social_media_details').modal('hide');
                    $('#upwrdz_soc_perm_modal').modal('hide');
                    $('[name="share_button"]')
                        .attr('onclick', "fb_share("+"'"+response.user_selected_role+"'"+")");
                    $('[name="cancel_share"]')
                        .attr('onclick', "navigate_to_page("+"'"+response.user_selected_role+"'"+")");
                    $("#soc_share_common_modal").modal({
                        show: true,
                        keyboard: false,
                        backdrop: 'static'
                    });
                }else if(response.log_usr_type == 'company_user'){
                    window.location = $('#id_company_url').val();
                }
                else if(response == "deactivated") {
                    alert('your account is not active call customer care');
                }else{
                    alert('Unable to Sign-In.\n Please Try after some time');
                }
            }
      });
    }else{
        check_social_email(fb_respnce_data.email);
    }
}

// Checking Logged-in Email and Facebook email both same or not to give the score to advisor
function check_social_email(email){
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
                advisor_scoring_facebook(email, fb_token);
            }else{
                alert('Please use same username for facebook ');
            }
        },error:function(response){
            alert('Unable process request. Please try after some time');
        }
    });
}

// Giving score to advisor for providing Facebook information to us
function advisor_scoring_facebook(email, fb_token){
  var token = csrf_token;
  $.ajax({
    type: "POST",
    url: "/reputation-index/advisor-scoring-fb/",
    beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", token);
    },
    data : {
        email  : email,
        access_token : fb_token
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

// Load the Facebook SDK asynchronously
(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


// after signup user will navigate according to user role/type and page type
function navigate_to_page(user_type=undefined){
    window.location.href = $('#next_url').val();
}