var csrf_token = $("#id_csrf_token").val();
var fb_token;

/**
 * @use: Login/Signup with Facebook
 * @param {String} (from_state) -> need to pass 'signup_or_login|member_login|social_auth'
 * @param {String} (user_type) - > need to pass 'advisor|member'
*/
function facebookMemberLogin(from_state, user_type=undefined){
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
                        member_get_user_details(from_state, fb_token, user_type);
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
        var page_type = $("input[name='page_type']").val();
        member_navigate_to_page(user_type, page_type);
    });
}

/**
 * @use: Getting user details from Facebook and Sending data to backend through ajax to 
 *      complete the signup/Login
 */
function member_get_user_details(from_state, fb_token, user_type){
    $("#check_fb_details").modal('hide');
    FB.api('/me',{fields:'first_name,last_name,email,gender,birthday,verified'},
        function(response) {
        var myBD = response.birthday;
        // Update Hidden inputs
        var birthday = "";
        if (typeof myBD != 'undefined'){
            var fb_date = response.birthday;
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
                url: "/login/investor_social_media_login/",
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                data : {
                    first_name : response.first_name,
                    last_name  : response.last_name,
                    email  : response.email,
                    birthday : birthday,
                    gender : response.gender,
                    source_media : 'facebook',
                    next_url : $('#next_url').val(),
                    user_type : user_type,
                    ref_link : referral,
                    token : fb_token,
                    social_auth : from_state,
                    inv_chk_login: $("[name='get_advice_hidden']").val(),
                    ad_chk_name: $("#id_ad_chk_f_name").val(),
                    ad_chk_email: $("#id_ad_chk_email").val(),
                    ad_chk_mob: $("#id_ad_chk_mobile").val(),
                    ad_chk_loc: $("#id_ad_chk_loc").val(),
                    ad_chk_country: $("[name='country_type']").val()
                },
                success:function(response) {
                    $('#signup-login-modal').modal('hide');
                    var page_type = $("input[name='page_type']").val();
                    $('#upwrdz_soc_perm_modal').modal('hide');
                    // if (response.exist_user == "new_user") {
                    //     shareContent();
                    // }
                    $('#check_social_media_details').modal('hide');
                    if ($("[name='user_type']").val() == "member" && !response.is_authenticated) {
                        show_verify_otp_modal_social_signup(response.profile_id, $('#next_url').val());
                    }
                    if (response == "deactivated") {
                        alert('your account is not active call customer care');
                    }
                }
          });
        }else{
            member_check_social_email(response.email);
        }
    });
}

// Checking Logged-in Email and Facebook email both same or not to give the score to advisor
function member_check_social_email(email){
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
                member_advisor_scoring_facebook(email, fb_token);
            }else{
                alert('Please use same username for facebook ');
            }
        },error:function(response){
            alert('Unable process request. Please try after some time');
        }
    });
}

// Giving score to advisor for providing Facebook information to us
function member_advisor_scoring_facebook(email, fb_token){
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
function member_navigate_to_page(user_type=undefined, page_type=undefined){
    if (user_type == 'member') {
        if (page_type == 'identity') {
            window.location.href = profile_link;
        } else if (page_type == 'repute') {
            window.location.href = repute_link;
        } else {
            window.location.href = $('#next_url').val();
        }
    } else {
        window.location.href = $('#next_url').val();
    }
}

// Showing Get advisor modal after completion of providing Social Media details
$('#soc_share_common_modal').on('hidden.bs.modal', function (e) {
    if (response.social_auth_ses 
        && response.inv_chk_login 
        && response.exist_user == "new_user"){
       get_advice();
   }
});
