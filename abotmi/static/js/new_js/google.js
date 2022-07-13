
var csrf_token = $("#id_csrf_token").val(); 
var auth2;
var googleLogin = function() {
    gapi.load('auth2', function(){
        // Retrieve the singleton for the GoogleAuth library and set up the client.
        auth2 = gapi.auth2.init({
            client_id: GOOGLE_CLIENT_ID,
            cookiepolicy: 'single_host_origin',
            scope: 'profile email'
        });
        attachSignin(document.getElementById('google_btn'));
    });
};
function attachSignin(element) {
    auth2.attachClickHandler(element, {},
        function(googleUserData) {
            googleUser(googleUserData, '');
        }, function(error) {
            // commented for now 
            //this callback function is for checking weather user deny the permission for google signup.
            // alert(JSON.stringify(error, undefined, 2));
        }
    );
}
// init google function
googleLogin();

//  Submitting users Google information
function googleUser(user, social_auth) {
    var token = csrf_token;
    var referral = "";
    if(is_advisor_clicked_google){
        user_type = 'advisor';
    }else{
        user_type = 'member';
    }
    $('#signup-login-modal').modal('hide');
    $.ajax({
        type: 'POST',
        url: "/login/social_media_login/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token );
        },
        data: {
            email           : user.getBasicProfile().getEmail(),
            name            : user.getBasicProfile().getName(),
            first_name      : user.getBasicProfile().getGivenName(),
            last_name       : user.getBasicProfile().getFamilyName(),
            profile_image   : user.getBasicProfile().getImageUrl(),
            source_media    : 'google',
            user_type       : user_type,
            next            : $('#next_url').val(),
            ref_link        : referral,
            social_auth     : social_auth
        },
        success: function(response) {
            var page_type = $("input[name='page_type']").val();
            if (response.exist_user == "user_exist" || response.exist_user == "new_user"){
                if (response.social_auth_ses && response.inv_chk_login){
                    get_advice();
                    $('#get-advice-modal').find('.close').remove();
                }
                $('#check_social_media_details').modal('hide');
                $('#upwrdz_soc_perm_modal').modal('hide');
                window.location.href = '/';
                if(user_type == 'member'){
                    $('#check_social_media_details').modal('hide');
                    $('#upwrdz_soc_perm_modal').modal('hide');
                }
            }else if(response == 'company_user'){
                window.location = $('#id_company_url').val();
            }else if(response == "deactivated"){
                alert('your account is not active call customer care');
            }else if(response == 'social_auth'){
                $('#upwrdz_soc_perm_modal').modal('hide');
                $('#check_social_media_details').modal('hide');
            }
            else{
                alert('Unable to Sign-In.\n Please try after some time');
            }
        },
    });
}
