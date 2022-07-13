// CSRF token initializing
var csrf_token = $("#id_csrf_token").val();

// open modal to Invites advisor to rate 
function invite_advisor_to_rate_modal(user_type){
    $("#client-ranking").hide();
    $("#peerrating-view").hide();
    $.ajax({
        type: "GET",
        url: "/dashboard/invite_advisor_to_rate/",
        data: {'user_type': user_type},
        success: function(response){
            $('#common_base_modal').html('');
            $('#common_base_modal').html(response);
            if(user_type=='advisor'){
                $("#title_span").html('INVITE PEER TO RATE');
            }
            else{
                $("#title_span").html('INVITE CLIENT TO RANK');
            }
            $('.modal-backdrop').remove();
            $('.blur').removeClass("blur");
            show_bootstrap_modal('#invite-rate-modal');
           
        }
    });
}

//Invites advisor to rate and save user details
function invite_advisor_to_rate(){
    var token = csrf_token;
    var validation_result=validate_data();
    if(validation_result == true){
        $("#invite_button").attr("disabled", true);
        $("#invite_button").html('<option> Processing ...</option>');
        var invite_advisor_to_rate_form_data=$('#hidden_values').val();
        $.ajax({
            type: "POST",
            url: "/dashboard/invite_advisor_to_rate/",
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {'invite_advisor_to_rate_form_data' : invite_advisor_to_rate_form_data},
            success: function(response){
                if(response=='success'){
                    $("#invite_button").attr("disabled", false);
                    $('#invite-rate-modal-body').html('<p class="text-center" style="font-size: 16px;">Invitation sent</p>');
                    window.location.reload();
                }
                else{
                    $('#invite-rate-modal-body').html('');
                    $('#invite-rate-modal-body').html('<p class="text-center">'+response+'</p>');
                }
            }
        });
    }
}

// Function validates and checks weather the email is already exist or not
function check_email_for_rating(emailfield){
    var missed = 0;
    email_id = document.getElementById(emailfield).value;
    var token = csrf_token;
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    var email = document.getElementById(emailfield);
    if(!re.test(email.value)) {
        email.focus;
        document.getElementById(emailfield).style.border='1px solid #C32F2F';
        document.getElementById('error'+emailfield).innerHTML = "Enter a valid email id";
    }else{
        $.ajax({
            type: "POST",
            url: "/signup/check_email/",
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", token);
            },
            data:{'username': email_id},
            success: function(response) {
                if(response=='true'){
                    document.getElementById('error'+emailfield).innerHTML = "";
                    document.getElementById(emailfield).style.border='';
                }
                else{
                    document.getElementById('error'+emailfield).innerHTML = "Email Already Exist.";
                    document.getElementById(emailfield).style.border='1px solid #C32F2F';
                    document.getElementById(emailfield).value="";
                    email_id.focus;
                }
            }
        });
    }
}
