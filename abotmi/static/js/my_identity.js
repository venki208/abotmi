// Global  variable declaration
var csrf_token = $("#id_csrf_token").val();
$(document).ready(function() {
    $("#peer_rating").rateit('value', rating_value);
    $("#consumer_ranking").rateit('value', ranking_value);
});
var id_modal = 1;
var edit_languages_button = $('#edit_languages_button');
var edit_promise_button = $("#id_edit_promise");
var edit_belief_button = $("#id_belief_button");
var edit_education_button = $("#education_button");
var edit_contact_details_button = $("#id_contact_details");
var edit_sales_accomplishments_button = $("#edit_sales_accomplishments");
var edit_self_declaration_button = $('#edit_self_declaration');
var edit_skills_button = $('#id_edit_skills');
var profile_pic = $("#id_profile_pic");
var edit_peer_connection_button = $("#edit_peer_connections");
var edit_client_connection_button = $("#edit_client_connections");
var edit_experience = $("#edit_experience");
var edit_certification = $("#a_edit_certification");

// Show bootstrap Modal function(pass id or name)
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show:true,
        keyboard:false,
        backdrop:'static'
    });
}

// activating my identiy menu   
$(document).ready(function(){
    $("#identity_menu").addClass("active");
})

// setting response data into common div
function load_data(response) {
    $("#my_identity_modal").html('');
    $("#my_identity_modal").html(response);
}

// opens advisor specialization pop up
function advisor_specialization(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/my_identity/get_advisory_specilization/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#my_identity_modal').html('');
            $('#my_identity_modal').html(response);
            show_bootstrap_modal('#id_advisor_specialization');
        }
    });
}

// Opens the regulatory registration pop up
function regulatory_registration(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/my_identity/edit_regulatory_registration/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#my_identity_modal').html('');
            $('#my_identity_modal').html(response);
            show_bootstrap_modal('#id_regulatory_registration');
        },
        error: function(response) {
            alert("Unable to view Regulatory Registration details. \n Please try again after sometime. ");
        }
    });
}

// Common script for validating one field
function validate_field(field_id, help_id, name){
    var is_valid = validate_field_onkeypress(field_id, help_id, name);
    if(is_valid !=0){
        return false;
    }else{
        return true;
    }
}

// Contact details Modal
edit_contact_details_button.on('click', function (e) {
    avoid_double_click('id_contact_details');
    $.ajax({
        method: 'GET',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        url: '/my_identity/edit_contact_details/',
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#contactDeailsModal');
        },
        error: function(response){
            alert('Unable to Process your request right now. \n Please try again after some time');
        }
    });
});

// modify the domain
function calendly_domian() {
    var calendly_link = $('#id_calendly').val();
    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
    if (!calendly_link.match(re)) {
        $("#help_id_calendly").html('Please Enter valid URL');
        $("#help_id_calendly").focus();
        return false;
    }else{
       if (!/^(f|ht)tps?:\/\//i.test(calendly_link)) {
           if (calendly_link.indexOf("www.") != 0) {
               $("#id_calendly").val('http://www.' + calendly_link);
           } else {
               $("#id_calendly").val('http://' + calendly_link);
           }
           $("#help_id_calendly").html('');
       } else if (!/((?:www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i.test(calendly_link)) {
           calendly_link = calendly_link.replace(/^http(s)?\:\/\//i, "");
           $("#id_calendly").val('http://www.' + calendly_link);
           $("#help_id_calendly").html('');
       }
        return true;
    }
}

// updates users contact details
function update_contact_details(){
    var contact_mobile_num = get_mobile_no("#id_contact_mobileno");
    var cont_city = $('#id_contact_city').val();
    var calendly_link = $('#id_calendly').val();
    var calendly_check = true;
    if ($('#id_calendly').val()){
        if(calendly_domian()){
            calendly_check = true;
        }else{
            calendly_check = false;
        }
    }
    if(validate_field('id_contact_mobileno', 'help_id_contact_mobileno', 'Mobile')
        && validate_field('id_contact_city', 'help_id_contact_city', 'City') && calendly_check==true) {
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token );
            },
            url: '/my_identity/update_contact_details/',
            data:{
                mobile: contact_mobile_num,
                city : cont_city,
                calendly: calendly_link
            },
            success: function(response){
                $("#mobile_content").html(contact_mobile_num);
                $("#city_content").html(cont_city);
                $("#id_org_city_span").html(cont_city);
                $("#cal_link")
                    .attr('href', calendly_link)
                    .html(calendly_link);
                $("#contactDeailsModal").modal('hide');
                if (!calendly_links || calendly_links == "None") {
                    window.location.reload();
                }
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

// Opens languages Modal
edit_languages_button.on('click', function (e) {
    avoid_double_click('edit_languages_button')
    $.ajax({
        method: 'GET',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        url: '/my_identity/edit_languages/',
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#languageModal');
        },
        error: function(response){
            alert('Unable to Process your request right now. \n Please try again after some time');
        }
    });
});

// Saves the language/s
function save_languages(){
    var languages = $("#id_languages").val();
    if(validate_field('id_languages', 'help_id_languages', 'Languages')){
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            url: '/signup/onchange_save_field/',
            data:{
                name: 'language_known',
                value: languages,
                username: username
            },
            success: function(response){
                $("#language_content").html(languages);
                $("#languageModal").modal('hide');
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

// Fucntion opens My Promise Modal
edit_promise_button.on('click', function(e){
    $.ajax({
        method: 'GET',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrf_token );
        },
        url: '/my_identity/edit_my_promise/',
        data: {},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#mypromiseModal');
        },
        error: function(response){
            alert('Unable to Process your request right now. \n Please try again after some time');
        }
    });
});

// It saves my promise
function save_my_promise(){
    var my_promise = $("#id_promise").val();
    if(validate_field('id_promise', 'help_id_promise', 'My Promise')){
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token );
            },
            url: '/signup/onchange_save_field/',
            data:{
                name: 'my_promise',
                value: my_promise,
                username: username
            },
            success: function(response){
                $("#promise_content").html(my_promise);
                $("#mypromiseModal").modal('hide');
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

// My Belief Modal
edit_belief_button.on('click', function(){
    avoid_double_click('id_belief_button');
    $.ajax({
        method: 'GET',
        url: '/my_identity/edit_my_belief/',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrf_token );
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#mybeliefModal');
        },
        error: function(response){
            alert('Unable to Process your request right now. \n Please try again after some time');
        }
    });
});

// Save my belief 
function save_my_belief(){
    var my_belief = $("#id_my_belief").val();
    if(validate_field('id_my_belief', 'help_id_my_belief', 'My Belief')){
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token );
            },
            url: '/signup/onchange_save_field/',
            data:{
                name: 'my_belief',
                value: my_belief,
                username: username
            },
            success: function(response){
                $("#my_belief_content").html(my_belief);
                $("#mybeliefModal").modal('hide');
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

// Edit Education Modal
function edit_educations(){
    var token = csrf_token;
    avoid_double_click('edit_education')
    $.ajax({
        type: "POST",
        url: "/signup/education/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        data:{
            page_type: 'education_edit_modal'
        },
        success: function(response){
            $('#my_identity_modal').html('');
            $('#my_identity_modal').html(response);
            show_bootstrap_modal('#educationModal');
        },
        error: function(response) {
            show_alert(
                'error',
                '',
                '<p>Unable to process your request \n Please try again after some time.</p>'
            );
        }
    });
}

// This function saves education details
function save_my_education(){
    var educational_detail = "";
    educational_detail = '{"school":"' + $('#school').val() + '", "qualification":"' + $("#qualification").val() + '","field_of_study":"' + $('#field_of_study').val() + '","activities":"' + $('#activities').val() + '","from_year":"' + $('#from_year').val() + '","to_year":"' + $('#to_year').val() + '","grade":"' + $('#grade').val() + '"}';
    if (validate_edit_education_form()) {
        $.ajax({
            method: "POST",
            url: '/my_identity/save_education/',
            beforeSend: setHeader,
            data: {
                'educational_details': educational_detail,
            },
            complete: function (e, xhr, settings) {
                var status = e.status;
                if (status == 200) {
                    $("#school_span").html($("#school").val());
                    $("#qualification_span").html($("#qualification").val());
                    $("#field_of_study_span").html($("#field_of_study").val());
                    $("#activities_span").html($("#activities").val());
                    $("#to_year_span").html($("#from_year").val());
                    $("#from_year_span").html($("#to_year").val());
                    show_alert(
                        'success',
                        'educationModal',
                        '<p>Successfully updated Education Details</p>'
                    );
                } else {
                    show_alert(
                        'error',
                        'educationModal',
                        '<p>Unable to Process your request right now. \n Please try again after some time</p>'
                    );
                }
            },
            error: function (response) {
                show_alert(
                    'error',
                    'educationModal',
                    '<p>Unable to Process your request right now. \n Please try again after some time</p>'
                );
            }
        });
    }
}

// my sale accomplishments modal
edit_sales_accomplishments_button.on('click', function(){
    $.ajax({
        method: 'GET',
        url: '/my_identity/edit_sales_accomplishments/',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrf_token );
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#id_mysale_accomplishments');
        },
        error: function(response){
            alert('Unable to Process your request right now. \n Please try again after some time');
        }
    });
});

// It saves my sale accomplishments
function add_sales_acomplishment(id,help_id){
    var sales_content_value = $("#"+id).val();
    var token = csrf_token;
    if(sales_content_value == ''){
        $('#'+id).addClass('not_valid');
        $("#"+help_id).html('Please Enter Sales Accomplishments');
        return false;
    }else{
        $('#'+id).removeClass('not_valid');
        $("#"+help_id).html('');
        $.ajax({
            method: "POST",
            url:'/my_identity/add_sales_acomplishments/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token );
            },
            data:{
                sales_content : sales_content_value
            },
            success:function(response){
                if(response == 'success'){
                    $('#id_main_my_sales_content').html(sales_content_value);
                    $("#id_mysale_accomplishments").modal('hide');
                }
            }
        });
    }
}

// self Declaration modal
edit_self_declaration_button.on('click', function(){
    avoid_double_click('edit_self_declaration')
    $.ajax({
        method:'GET',
        url: '/my_identity/edit_self_declaration/',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', token);
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#id_show_self_declaration');
        },
        error: function(response){
            alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});

// It saves self declaration content
function add_self_declaration(id, help_id){
    var about_me_content = $('#'+id).val();
    var token = csrf_token;
    if(about_me_content == ''){
        $('#'+id).addClass('not_valid');
        $('#'+help_id).html('Please enter Self Declaration');
        return false;
    }else{
        $('#'+id).removeClass('not_valid');
        $("#"+help_id).html('');
        $.ajax({
            method: 'POST',
            url: '/my_identity/add_self_declaration/',
            beforeSend: function(request){
                request.setRequestHeader('X-CSRFToken', token);
            },
            data:{
                self_declaration_content: about_me_content
            },
            success: function(response){
                if(response == 'success'){
                    $('#id_main_about_me_content').html(about_me_content);
                    $('#id_show_self_declaration').modal('hide');
                }
            }
        });
    }
}

// facebook share function
function fb_share(){
    var page = advisor_profile_url;
    var fbpopup = window.open("https://www.facebook.com/sharer/sharer.php?u="+page, "pop", "width=600, height=400, scrollbars=no");
}

// facebook LinkedIn function
function LinkedInShare() {
    window.open("https://www.linkedin.com/shareArticle?mini=true&url="+advisor_profile_url+"&title=UPWRDZ&summary=My%20UPWRDZ%20Shared%20Profile&source=LinkedIn",'linkedin','height=400,width=600');
}

// facebook googleplus function
function googleplusbtn() {
    window.open('https://plus.google.com/share?url=' +advisor_profile_url+'','','menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=200,width=600');
    return false;
}

// facebook twitter function
function twitter_share(){
    var width  = 575,
        height = 400,
        left   = ($(window).width()  - width)  / 2,
        top    = ($(window).height() - height) / 2,
        url = "https://twitter.com/intent/tweet?url=" + advisor_profile_url,
        opts   = 'status=1' +
                    ',width='  + width  +
                    ',height=' + height +
                    ',top='    + top    +
                    ',left='   + left;

    window.open(url, 'twitter', opts);
    return false;
}

// open edit skills modal
edit_skills_button.on('click', function(){
    avoid_double_click('id_edit_skills')
    $.ajax({
        method:'GET',
        url: '/my_identity/edit_skills/',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', token);
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#id_skills_modal');
        },
        error: function(response){
            alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});

// save skills for advisor
function add_skills(id, help_id){
    var skills_arr = [];
    $.each($("input[name='skills_checked']:checked"), function(){
        skills_arr.push($(this).val());
    });
    var boxes = $("input[name='others_main_checked']:checked");
    if(boxes.length == 1){
        skills_arr.push($("#others_main_id").val());
    }
    var skills_content = skills_arr.join(",");
    var token = csrf_token;
   
   if(validate_skills()){
       $('#'+id).removeClass('not_valid');
       $("#"+help_id).html('');
       $.ajax({
           method: 'POST',
           url: '/my_identity/add_skills/',
           beforeSend: function(request){
               request.setRequestHeader('X-CSRFToken', token);
           },
           data:{
               skills_content: skills_content
           },
           success: function(response){
               if(response == 'success'){
                   $('#id_main_skills_content').html('');
                   for (i=0; i< skills_arr.length; i++){
                       var curr_skill;
                       if((i+1) < skills_arr.length){
                           curr_skill = skills_arr[i]+'  |  ';
                       }else{
                           curr_skill = skills_arr[i];
                       }
                       $('#id_main_skills_content').append(curr_skill);
                   }
                   $('#id_skills_modal').modal('hide');
               }
           }
       });
   }
}

// Edit/View Image modal
profile_pic.on('click', function(){
    $.ajax({
        method:'GET',
        url: '/my_identity/edit_or_view_image/',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', token);
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#imageModal');
        },
        error: function(response){
            alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});

// edit peer connection modal
edit_peer_connection_button.on('click', function(){
    $.ajax({
        method:'GET',
        url: '/my_identity/edit_peer_connection/',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', token);
        },
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#peer_connection_modal');
        },
        error: function(response){
            alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});

// save total advisors connected count
function save_peer_connection(){
     var peer_conn = $("#id_peer_connection").val();
    if(validate_field('id_peer_connection', 'help_id_peer_connection', 'total advisors connected')){
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            url: '/my_identity/save_peer_connections/',
            data:{
                total_advisors_connected : peer_conn
            },
            success: function(response){
                $("#total_advisors_connected_count").html(peer_conn);
                $("#peer_connection_modal").modal('hide');
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

// edit client connection modal
edit_client_connection_button.on('click', function(){
    $.ajax({
        method: 'GET',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        url: '/my_identity/edit_client_connection/',
        data:{},
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#client_connection_modal');
        },
        error: function(response){
             alert("Unable to Process your request right now. \n Please try again after some time'");
        }
    });
});

// save total clients served count
function save_client_connection(){
     var client_connections = $("#id_client_connection").val();
    if(validate_field('id_client_connection', 'help_id_client_connection', 'total clients served')){
        $.ajax({
            type: 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            url: '/my_identity/save_client_connections/',
            data:{
                total_client_serverd_count : client_connections
            },
            success: function(response){
                $("#total_clients_served_count").html(client_connections);
                $("#client_connection_modal").modal('hide');
            },
            error: function (response) {
                alert('Unable to save. \n Please Try again after some time');
            }
        });
    }
}

//send/share profile link modal
function load_share_profile_by_email_modal() {
    avoid_double_click('profile_share');
    $.ajax({
        type: 'GET',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: '/my_identity/share_profile_by_email/',
        data: {},
        success: function (response) {
            load_data(response);
            show_bootstrap_modal('#share_profile_by_email');
        },
        error: function (response) {
            alert('Unable to process your request right now.\n Please try again after some time');
        }
    });
}

// Function submits the otp
function submit_otp() {
    var otp_verification_status = verify_and_submit_otp();
    if (otp_verification_status){
        otp_verification_status.success(function (response) {
            if (email_signup == 'True' && response.status == '200') {
                if (response.is_mobile_otp) {
                    $("#otp_verified_message_model").modal('hide');
                } else {
                    $('#help_text_id_otp').html('Please enter valid OTP');
                }
            } else if (email_signup != 'True' && response.status == '200') {
                if (response.is_email_otp && response.is_mobile_otp) {
                    $("#otp_verified_message_model").modal('hide');
                } else {
                    if (!response.is_email_otp) {
                        $('#help_text_id_email_otp').html('Please enter valid email OTP');
                    } else {
                        $('#help_text_id_email_otp').html('');
                    }
                    if (!response.is_mobile_otp) {
                        $('#help_text_id_otp').html('Please enter valid mobile OTP');
                    } else {
                        $('#help_text_id_otp').html('');
                    }
                }
            } else {
                $('#help_text_id_email_otp').html('Please enter valid email OTP');
                $('#help_text_id_otp').html('Please enter valid mobile OTP');
            }
        });
        otp_verification_status.error(function (response) {
            alert('Unable to validate OTP right now \n Please try again after some time');
        });
    }
}

// Function for Loding modal to view or change the batch
function change_batch_code() {
    $("#id_cp_badge").removeAttr('disabled');
    $.ajax({
        method: 'GET',
        url: '/my_identity/batch_code/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{},
        success: function(response){
            $("#batch_url_div").html('');
            $("#batch_url_div").html(response);
            $("#batch_img_div").addClass('hide');
        },
        error: function(response){
            alert('Unable to Update the Batch code \n Please try again after some time');
        }
    });
}

// Getting Profile attachment Modal
function profile_attach(){
    $.ajax({
        type: "GET",
        url: '/my_identity/profile_attachment/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function(response){
            $('#profile_attachment_modal_div').html('');
            $('#profile_attachment_modal_div').html(response);
            show_bootstrap_modal('#profile_attach1');
        }
    });
}

// View followees list and search for the advisors
function view_followers() {
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/view_followers/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function (response) {
            load_data(response);
            document.getElementById("heading").innerHTML = "FOLLOWING";
            show_bootstrap_modal('#unfollow_advisors_list');
        }
    });
}

//Connects investor to the advisor
function connect_advisor(){
    var token = csrf_token;
    var member_code = 'd0198504366a7626e1722df6c867158d';
    var q_id = 3;
    $.ajax({
        type: "POST",
        url: "/member/connect_advisor/",
        data:{ member_code : member_code, q_id : q_id },
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function (response) {
            alert("Done");
        }
    });
}

// Script fo whatsapp share
function whatsappshare() {
    if( isMobile.any() ) {
        var text = $(this).attr("data-text");
        var url = $(this).attr("data-link");
        var message = encodeURIComponent(text) + " - " + encodeURIComponent(url);
        var whatsapp_url = "whatsapp://send?text="+advisor_profile_url;
        window.open(whatsapp_url, '_blank');
    } else {
        ///web whatsapp functionality
        var text = $(this).attr("data-text");
        var url = $(this).attr("data-link");
        var message = encodeURIComponent(text) + " - " + encodeURIComponent(url);
        var whatsapp_url = "http://web.whatsapp.com/send?text="+advisor_profile_url;
        window.open(whatsapp_url, '_blank');
    }
}

// Experience
edit_experience.on('click', function(e){
    avoid_double_click('edit_experience')
    $.ajax({
        method: 'GET',
        url: '/my_identity/experience/',
        beforeSend: setHeader,
        success: function(response){
            load_data(response);
            show_bootstrap_modal('#editExperience');
        },
        error: function(e){
            show_alert(
                'error',
                '',
                'Unable to process your request'
            );
        }
    });
});

function save_experience(){
    if (validate_field_onkeypress('experience', 'help_experience', 'Total Experience') == 0){
        $.ajax({
            method: 'POST',
            url: '/my_identity/save_experience/',
            beforeSend: setHeader,
            data: {
                'experience': $("#experience").val()
            },
            success: function (e, xhr, settings){
                if(settings.status == 200){
                    $("#total_experience_span").html($("#experience").val());
                    show_alert(
                        'success',
                        'editExperience',
                        '<p>Experience Updated Successfully</p>'
                    );
                }else{
                    show_alert(
                        'error',
                        'editExperience',
                        '<p>Unable to update Experience \n Please try again after sometime.</p>'
                    );
                }
            },
            error: function(e){
                show_alert(
                    'error',
                    'editExperience',
                    '<p>Unable to update Experience \n Please try again after sometime.</p>'
                );
            }
        });
    }
}

// Edit Certification --> Loading Edit certification modal
edit_certification.on('click', function (e) {
    avoid_double_click('a_edit_certification')
    $.ajax({
        type: "POST",
        url: "/signup/education/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        data: {
            page_type: 'certification_edit_modal'
        },
        success: function (response) {
            $('#my_identity_modal').html('');
            $('#my_identity_modal').html(response);
            show_bootstrap_modal('#certificationModal');
        },
        error: function (response) {
            show_alert(
                'error',
                '',
                '<p>Unable to process your request \n Please try again after some time.</p>'
            );
        }
    });
});

// Saving/updating the certifications
function save_certification(){
    if (validate_certification_form() == 0) {
        var certification_detail = get_certificate_json();
        certification_detail_json = JSON.stringify(certification_detail);
        $.ajax({
            method: 'POST',
            url: '/my_identity/save_certification/',
            beforeSend: setHeader,
            data:{
                certification_data: certification_detail_json
            },
            success: function (e, xhr, settings){
                if(settings.status == 200){
                    // $('#cert_name_span').html($('#certification_name').val());
                    // $('#certi_auth_span').html($('#certi_authority').val());
                    // $('#certi_lic_no').html($('#licence_number').val());
                    // $('#cert_url_span').html($('#certi_url').val());
                    // $('#cert_from_year_span').html($('#certificate_from_year').val());
                    // $('#cert_to_year_span').html($('#certificate_to_year').val());
                    show_alert(
                        'success',
                        'certificationModal',
                        '<p>Successfully updated Certifications Details</p>',
                        'reload:true'
                    );
                }else{
                    show_alert(
                        'error',
                        'certificationModal',
                        '<p>Unable updated Certifications Details. \n Please try again after sometime.</p>'
                    );
                }
            },
            error: function(response){
                show_alert(
                    'error',
                    'certificationModal',
                    '<p>Unable updated Certifications Details. \n Please try again after sometime.</p>'
                );
            }
        });
    }

}
