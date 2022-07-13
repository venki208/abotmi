var csrf_token = $("#id_csrf_token").val();
var from_state = "";
var linkedin_user_type = '';

// Setup an event listener to make an API call once auth is complete
function onLinkedInLoad(from_state, user_type=undefined) {
    localStorage.removeItem('from_state_for_ln');
    localStorage.setItem('from_state_for_ln', from_state);
    from_state = from_state;
    linkedin_user_type = user_type;
    IN.UI.Authorize().place();
    IN.Event.on(IN, "auth", onLinkedInAuth);
}

// Use the API call wrapper to request the member's basic profile data
function onLinkedInAuth() {
    IN.API.Profile("me")
    .fields("firstName", "lastName", "industry", "location:(name)", "picture-url", "headline", "summary", "num-connections", "public-profile-url", "distance", "positions", "email-address", "educations","date-of-birth")
    .result(displayProfiles)
    .error(displayProfilesErrors);
}

// Submitting the success data from Linkedin
function displayProfiles(profiles) {
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
        url : "/login/investor_social_media_login/",
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
            var page_type = $("input[name='page_type']").val();
            if (response.social_auth_ses) {
                $('#upwrdz_soc_perm_modal').modal('hide');
                $('#check_social_media_details').modal('hide');
            }
            // show the get advice pop up when the investor clicks the same
            if (response.social_auth_ses && response.inv_chk_login){
                get_advice();
            }
            if(response == "deactivated"){
                alert('your account is not active call customer care');
            }
        }
      });
    }else{
        check_social_email_for_linkedin(email, headline, summary);
    }
}

// Checking Login email id and Linked in email id are same or not
function check_social_email_for_linkedin(email, headline, summary){
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
                advisor_scoring_linedin(email, headline, summary);
            }else{
                alert('Please use same username for linkedin');
            }
        },error:function(response){
            alert('Unable process request. Please try after some time');
        }
    });
}

// Adding score for sharing Linkedin information 
function advisor_scoring_linedin(email, headline, summary){
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
function displayProfilesErrors(error) {
    profilesDiv = document.getElementById("fetch_data");
    profilesDiv.innerHTML = error.message;
}

// Sharing the UPWRDZ content to users Linkedin wall
function shareContent() {
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
      .result(onSuccess)
      .error(onError);
}

function onSuccess(data) {
    var data = data;
}

function onError(error) {
    var error = error;
}
