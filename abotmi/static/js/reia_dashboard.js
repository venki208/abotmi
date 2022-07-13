// Global variable initialization
var csrf_token = $("#id_csrf_token").val();
var token = csrf_token;
var identity_pack = $("#id_identity_pack");
$("#id_create_vedio").bind('click', [], video_shoot_request_modal);
var calendly = $("#id_calendly").val();

$(document).ready(function () {
    $("#peer_rating").rateit('value', rating_value);
    $("#consumer_ranking").rateit('value', ranking_value);
});

// Function advisor's index
function get_advisor_index(){
  $.ajax({
      type: 'POST',
      url: '/reputation-index/get_reputation_index_data/',
      data:{},
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrf_token);
      },
      success: function (response) {
        $("#dashboard_modal").html('');
        $("#dashboard_modal").html(response);
        show_bootstrap_modal('#reputation_index_modal');
      },
      error: function (response) {
          alert('Unable to process your request now. Please try again after some time');
      }
  });
}
// $('.vticker').easyTicker({
//     height: '75px'
// });

// checking advisor is uploaded address proof or not
function check_address_proof() {
    var is_eipv_completed;
    return $.ajax({
        type: 'POST',
        url: '/dashboard/check_address_proof/',
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{}
    });
}

// CRISIL Scripts
// Check EIPV is completed or not and Show Apply Now CRISIL Modal
function show_apply_crisil_modal(id){
    var is_eipv_completed = check_address_proof();
    is_eipv_completed.success(function(data){
        if(data == "true"){
            $.ajax({
                type: 'GET',
                url: '/dashboard/load_apply_now_crisil_modal/',
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                success: function (response) {
                    $("#dashboard_modal").html('');
                    $("#dashboard_modal").html(response);
                    $("#crisil_modal").modal('show');
                },
                error: function (response) {
                    alert('Unable to process your request now. Please try again after some time');
                }
            });
        }else{
            var confirm_request = confirm("CRISIL needs e-IPV process mandatory, You didn't Complete e-IPV Process.\n Do you want to do now?");
            if(confirm_request == true){
                window.location.href = "/signup/submit_eipv_doc/";
            }
        }
    });
    is_eipv_completed.error(function(data){
       alert("Some error occured, Please try again after some time.");
    });
}

// Show CRISIL Offer
function show_offer(){
    $('#to_get_offers').toggle();
    $("#crisil_modal_body_content").toggleClass('crisil_modal_body_height');
}

// caculating gross total according to selected years of CRISIL
function calculate_gross_total(id) {
    var gross_total = certificate_cost;
    var final_gross_total = $('#'+id).val()*gross_total;
    var final_gross_total_value = convert_value_to_comma_seperated(final_gross_total);
    var final_tax = (final_gross_total)*(crisil_tax_percentage/100);
    var final_tax_value = convert_value_to_comma_seperated(final_tax);
    var final_amount = final_gross_total+final_tax;
    var final_amount_value = convert_value_to_comma_seperated(final_amount);
    if($('#'+id).val() != 2){
        $("#id_actual_cross_amount").html('');
        $("#id_offer_label").html('NA');
    }else{
        $('#id_actual_cross_amount').html('<span><i class="fa fa-inr" aria-hidden="true" style="opacity:0.8;"></i></span>33,000');
        $("#id_offer_label").html('Pay 2 & Get 3');
    }
    $('#id_gross_total').html('<span><i class="fa fa-inr" aria-hidden="true" style="opacity:0.8;"></i></span>'+final_gross_total_value);
    $("#id_tax").html(" &#8377;"+final_tax_value);
    $("#id_total_amount").html(' <span><i class="fa fa-inr" aria-hidden="true" style="opacity:0.8;"></i></span>'+final_amount_value);
}

// Give value with comma seperated
function convert_value_to_comma_seperated(value) {
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// checking confirmation from advisor to go with years which advisor Selected in apply now popup
function confirm_advisor_to_apply_crisil() {
    var crisil_selected_years_range = $("#id_crisil_year_range").val();
    var confirm_request = confirm("You have selected the term as "+crisil_selected_years_range+" year(s). \nDo you wish to continue?");
    if(confirm_request == true){
        appling_crisil();
    }
}

// CRISIL Application process
function appling_crisil(){
    var token = csrf_token;
    $("#id_crisil").removeAttr("onclick");
    $("#crisil_modal_body_content").removeAttr("onscroll");
    $("#id_crisil").html('Please Wait...');
    $('#id_crisil').prop('disabled', true);
    $("#id_crisil_cancel").prop('disabled',true);
    $('#id_apply_promocode').prop('disabled',true);
    var crisil_thanks_information = $("#crisil_thanks_information").html();
    $.ajax({
        type:'POST',
        url : '/dashboard/appling_crisil/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        data:{
            username : username,
            promocode : $('#id_promocode').val(),
            crisil_selected_years : $("#id_crisil_year_range").val(),
            promocode_status : $('#id_promocode_status').val()
        },
        success : function(response){
            if(response == 'success'){
                $('#crisil_modal_body').html('');
                $('#crisil_modal_body').html(crisil_thanks_information);
                $("#crisil_modal").modal('show');
            } else {
                alert('Unable to proces your request.\n please try again later');
            }
        },
        error:function(response){
        }
    });
}

// Load CRISIL Payment Modal
function load_crisil_payment_modal(){
    var token = csrf_token;
    $.ajax({
        type: 'GET',
        url: '/dashboard/submit_crisil_form/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            $('#id_description').val(no_of_years_selected);
            $('#crisil_transaction').modal('show');
        }
    });
}

// Load CRISIL Renewal Payment
function load_crisil_renewal_payment_modal(){
    $.ajax({
        type: 'GET',
        url: '/dashboard/renewal_submit_crisil_form/',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            $('#crisil_renewal').modal('show');
        }
    });
}

// Cheking advisor is subscribed Video Shoot and loading package modal/video request modal
function video_shoot_request_modal(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/check_advisor_subscribed_to_create_video/",
        data: {},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            if(response.res){
                load_video_request_modal();
            }else{
                micro_learning_packages_model();
            }
        }
    });
}

// Function for loading Video request modal
function load_video_request_modal(){
    $.ajax({
        type: 'POST',
        url: '/dashboard/get_video_request_modal/',
        beforeSend: setHeader,
        data:{},
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#video-request-modal');
        },
        error: function(response){
            alert('Unable to Process your request \n Please try again after some time');
        }

    });
}

// Function shows pinocde modal
function show_check_pincode_model(){
    show_bootstrap_modal('#pincode_confirmation_modal');
    initMap();
}

//confirmation popup to cancel the pincode
function cancel_pincode_confirmation_popup(){
    $('#current_pincode').val("");
    $('#pincode_confirmation_modal').modal('hide');
}

//validates pincode with regx
function validate_pin(pin){
    return /^[1-9]\d{3}$|^[1-9]\d{5}$/.test(pin);
}

//api call - transit hyperlocal
function transit_hyperlocal_api_call(){
  var pincode = $('#current_pincode').val();
  if(validate_pin(pincode)){
    localStorage.setItem("current_pincode", pincode);
    $.ajax({
      type: "POST",
      url: "/reputation-index/advisor_reputation_for_hyperlocal/",
      beforeSend: function(request){
        request.setRequestHeader("X-CSRFToken", csrf_token);
      },
      data: {"pincode":pincode,"hyperlocal_type":"transient"},
      success: function(response) {
        alert(response.message);
        cancel_pincode_confirmation_popup();
      }
    });
  }else{
    alert("pincode should be 4 or 6 digit number");
  }
}

// Upload video function in step 5
function upload_my_video(modal_id, div_modal_id){
    var token = csrf_token;
    $.ajax({
        type:"GET",
        url:"/dashboard/video_publish_modal/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success:function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal("#video-upload-modal");
        }
    });
}

// Validate video shoot form
function validate_video_shoot_form(){
    var is_mic_titl = validate_field_onkeypress('microlearning_tittle', 'help-text-microlearning-tittle', 'Title');
    var is_desc = validate_field_onkeypress('descrition_of_the_topic', 'help-text-descrition_of_the_topic', 'Description');
    var is_location = validate_field_onkeypress('microlearning_location', 'help-text-microlearning-location', 'Location');
    var is_date_of_shoot = $("#preffered_date_of_shoot").val();
    if(is_date_of_shoot==""){
        $("#help-text-preffered-date-of-shoot").html('Please enter preffered date of shoot');
        $("#preffered-date-of-shoot").addClass("not_valid");
        $("#preffered-date-of-shoot").focus();
    }else{
        $("#help-text-preffered-date-of-shoot").html('');
        $("#preffered-date-of-shoot").removeClass('not_valid');
        $("#preffered-date-of-shoot").focus();
    }
    if(is_mic_titl !=0
        || is_desc != 0 || is_location != 0 || is_date_of_shoot==""){
        return false;
    }else{
        return true;
    }
}

//modal for video shoot request
function video_shoot_request(){
    var microlearning_tittle = document.getElementById('microlearning_tittle').value;
    var descrition_of_the_topic = document.getElementById('descrition_of_the_topic').value;
    var microlearning_location = document.getElementById('microlearning_location').value;
    var preffered_date_of_shoot = $("#preffered_date_of_shoot").val();
    var animation_required = document.getElementById("animation_required").checked;
    var status="";
    if(animation_required==true){
        status = "Approved";
    }else{
        status = "Requested";
    }
    if (validate_video_shoot_form()) {
      $.ajax({
        type:"POST",
        url:"/dashboard/video_shoot_request/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", csrf_token);
        },
        data:{
            microlearning_tittle:microlearning_tittle,
            descrition_of_the_topic:descrition_of_the_topic,
            microlearning_location:microlearning_location,
            preffered_date_of_shoot:preffered_date_of_shoot,
            animation_required:status,
        },
        success:function(response){
            $('#video-request-modal').modal('hide');
        }
      });
    }
}

// views loop pop up
function view_loop(user_id){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/view_loop/",
        data: {user_id:user_id},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#view-loop-modal');
        }
    });
}

// Show do not follow pop up
function view_do_not_follow() {
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/view_followees/",
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function (response) {
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            document.getElementById("heading").innerHTML = "DO NOT FOLLOW";
            show_bootstrap_modal('#unfollow_advisors_list');
        }
    });
}

// Invite the new user to join as advisor in NF
function refer_advisor(){
    $.ajax({
        type: "POST",
        url: "/dashboard/refer_advisor/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            $('#advisor-loop').hide();
            $('.modal-backdrop').remove();
            $('.blur').removeClass("blur");
            show_bootstrap_modal('#refer-advisor-modal');
        }
    });
}

// Saving refer advisor
function save_refer_advisor() {
    var validation_result = validate_all();
    if (validation_result == true) {
        refreshtable();
        var table = html_to_json();
        $("#loop_advisor").attr("disabled", true);
        $("#loop_advisor").html('<option> Processing ...</option>');
        $.ajax({
            type: "POST",
            url: "/dashboard/save_refer_advisor/",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: {
                jsondata: table
            },
            success: function (response) {
                if (response == 'success') {
                    $("#loop_advisor").attr("disabled", false);
                    $('#refer-advisor-modal-body').html(
                        '<p class="text-center" style="font-size:16px;">Loop successful</p>'
                    );
                    window.location.reload();
                } else {
                    $('#refer-advisor-modal-body').html(
                        '<p>Unable to Loop/Refer Advisor <br />' +
                        ' Please try again after sometime</p>'
                    );
                }
            },
            error: function (response) {
                $('#refer-advisor-modal-body').html(
                    '<p>Unable to Loop/Refer Advisor <br />' +
                    ' Please try again after sometime</p>'
                );
            }
        });
    }
}

// Creating referal data to json
function html_to_json() {
    var json = '{';
    var otArr = [];
    var tbl2 = $('#loop_list tbody tr').each(function (i) {
        x = $(this).children();
        var itArr = [];
        x.each(function () {
            itArr.push('"' + $(this).text() + '"');
        });
        otArr.push('"' + i + '": [' + itArr.join(',') + ']');
    })
    json += otArr.join(",") + '}'

    return json;
}


// Shows client ranking pop up
function view_client_ranking(user_id,user_type){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/view_ranking_or_rating/",
        data: {user_id:user_id,user_type:user_type},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            if(user_type=='advisor'){
                $("#title_span_view").html('VIEW PEERS');
            }
            else{
                $("#title_span_view").html('VIEW CLIENTS');
            }
            show_bootstrap_modal('#view-rank-client-modal');
        }
    });
}

// function opens add member pop up
function add_member(user_id){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/add_member/",
        data: {user_id:user_id},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#add-member-modal');
        }
    });
}

//fucntion opens view member modal
function view_member(){
    $.ajax({
        type: "GET",
        url: "/dashboard/view_members/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#view-member-modal');
        }
    });
}

//fucntion opens client enquiry modal
function client_enquiry(user_id){
   var token = csrf_token;
   $.ajax({
       type: "POST",
       url: "/dashboard/client_enquiry/",
       data: {user_id:user_id},
       beforeSend: function(request){
           request.setRequestHeader("X-CSRFToken", token);
       },
       success: function(response){
           $('#dashboard_modal').html('');
           $('#dashboard_modal').html(response);
           show_bootstrap_modal('#enquiry-modal');
       }
   });
}

// modal shows user roles, that can be choosen in UPLYF
function choose_user_role(){
    $("#uplyf_user_role").modal('show');
}

// Modal to choose user role
function user_selection(){
    var user;
    if(document.getElementById("optionsRadios1").checked == true){
            user = document.getElementById('optionsRadios1').value;
        }
    else{
            user = document.getElementById('optionsRadios2').value;
        }
    launch_uplyf(user);
    $("#uplyf_user_role").modal('hide');
}

// launch UPLYF application from UPWRDZ
function launch_uplyf(user){
    var token = csrf_token;
    var is_eipv_completed = check_address_proof();
    var user_role = user;
    var advisor_reffer_client = registered_members_in_uplyf;
    is_eipv_completed.success(function(data){
        if(data == "true"){
            if(advisor_reffer_client != 0){
                var url_link = create_uplyf_session_url;
                $("#id_launch_uplyf_button").attr('disabled', true);
                $.ajax({
                    url: url_link,
                    type: 'POST',
                    beforeSend: function (request){
                        request.setRequestHeader("X-CSRFToken",token);
                    },
                    data:{user_role:user_role},
                    success: function(response_dict){
                        if(response_dict.status == true){
                            var x = document.getElementById("form_div");
                            var createform = document.createElement('form');
                            url = uplyf_server_name;
                            createform.setAttribute("action",url);
                            createform.setAttribute("method", "post");
                            createform.setAttribute("class", "form_name");
                            createform.setAttribute("id", "form_id");
                            x.appendChild(createform);

                            var inputelement = document.createElement('input');
                            inputelement.setAttribute("type", "text");
                            inputelement.setAttribute("name", "token");
                            inputelement.setAttribute("value", response_dict.token);
                            createform.appendChild(inputelement);

                            var input_username = document.createElement('input');
                            input_username.setAttribute("type", "text");
                            input_username.setAttribute("name", "username");
                            input_username.setAttribute("value", response_dict.username);
                            createform.appendChild(input_username);

                            var input_user_token = document.createElement('input');
                            input_user_token.setAttribute("type", "text");
                            input_user_token.setAttribute("name", "user_token");
                            input_user_token.setAttribute("value", response_dict.user_token);
                            createform.appendChild(input_user_token);

                            var input_user_role = document.createElement('input');
                            input_user_role.setAttribute("type", "text");
                            input_user_role.setAttribute("name", "users_role");
                            input_user_role.setAttribute("value", response_dict.users_role);
                            createform.appendChild(input_user_role);

                            document.getElementById("form_id").submit();
                        } else {
                            alert('The server could not be reached at this moment.. Please try after some time');
                            $("#id_launch_uplyf_button").attr('disabled', false);
                        }
                    }
                });
            }
            else{
                $("#id_advisor_count_client_modal").modal('show');
            }
        }else{
            var confirm_request = confirm("You didn't Complete e-IPV Process.\n Click Ok to complete the e-IPV Process.");
            if(confirm_request == true){
                window.location.href = "/signup/submit_eipv_doc/";
            }
        }
    });
}

// ajax call to open send group email modal
function load_send_group_email_modal(){
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/load_send_group_email_modal/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#send-group-email-modal');
        }
    });
}

//Modal opens crisil_terms_conditions
function call_crisil_terms_conditions() {
    $.ajax({
        type:"GET",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: "/dashboard/crisil_terms_and_conditions/",
        data:{},
        success:function (response) {
            $("#dashboard_modal").html(response);
            $('.modal-backdrop').remove();
            $('.blur').removeClass("blur");
            show_bootstrap_modal('#crisil_terms_conditions');
        },
        error:function(response) {
        },
    });
}

//shows advisor list to rate
function advisor_to_rate_list(){
    $.ajax({
        type: "GET",
        url: "/dashboard/advisor_rating_list/",
        success: function(response){
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#rate-modal');
        }
    });
}

//opens advisor_rate_modal
function advisor_rate_modal(activation_key){
    $.ajax({
        type: "GET",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: "/dashboard/rate_advisor/?activation_key="+activation_key,
        success: function(response){
            $('#rate_modal_body').html('');
            $('#rate_modal_body').html(response);
        }
    });
}

// Common modal to bring the pop up
function show_bootstrap_modal(elem) {
    $(elem).modal({
        show:true,
        keyboard:false,
        backdrop:'static'
    });
}

//Modal lists list enquiried clients
function list_enquiried_clients(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/list_enquiried_clients/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            $('#enquired_members_list_modal').modal({
                show: true
            });
        }
    });
}

//Modal lists view clients
function list_profile_viewed(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/list_profile_viewed/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#list_view_client_modal');
        }
    });
}

//Modal lists connect clients
function list_connect_profile(){
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/dashboard/list_connect_profile/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#list_connect_modal');
        }
    });
}

//Modal gets the transaction details
function manage_transaction() {
    var token = csrf_token;
    $.ajax({
        type:'POST',
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        url: "/dashboard/manage-uplyf-transaction/",
        success:function (response) {
            $("#dashboard_modal").html('');
            $("#dashboard_modal").html(response);
            show_bootstrap_modal('#manage_transaction_modal');
        },
        error: function (response){
            alert('unable to view Transactions');
        }
    });
}

// Uploads the transaction documents
function upload_transaction_documents(document_id){
    var token = csrf_token;
    var docs = document.getElementById("document_t"+document_id).files;
    var r_trans_id = document.getElementById("r_id"+document_id).value;
    if (docs && r_trans_id){
        for (var i = 0; i < docs.length; ++i) {
            var fd = new FormData();
            fd.append('r_trans_doc', docs[i]);
            fd.append('r_trans_id', r_trans_id);
            $.ajax({
                type: "POST",
                url: "/dashboard/upload_transaction_documents/",
                beforeSend: function(request){
                    request.setRequestHeader("X-CSRFToken", token);
                },
                data:fd,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(response){
                    if(response == 'True'){
                        alert(docs[i].name+' Document uploaded successfully');
                        $("#trans_uploaded_div").append("<span class='file-name'>"+docs[i].name+" ,</span>");
                        $("#document_t"+document_id).val('');
                    }else{
                        alert('unable to upload '+docs[i].name);
                    }
                }
            });
        }
    }else{
        alert('Please choose a file/files.');
    }
}

// ---my identity js methods --------
// Common modal for email acknowledment
function email_send_modal() {
    $('#send_modal').modal('show');
}

// microlearning faq modal
function get_microlearning_faq_modal(){
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/micro_learning_faq_modal/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            $('#video-upload-modal').modal('hide');
            $('.modal-backdrop').remove();
            $('.blur').removeClass("blur");
            show_bootstrap_modal('#micro_learning_faq_modal');
        }
    });
}

//Modal for crisil faq
function show_crisil_faq_modal(){
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/crisil_faq/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken", token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#crisil_faq_modal');
        }
    });
}

// Modal opens premium subscripttion details
function try_premium_modal() {
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/subscribe/profile-viewed-details/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#try_premium');
        }
    });
}

//Modal shows micro learning packages
function micro_learning_packages_model() {
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/micro_learning_packages_model/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#micro_learning_packages');
        }
    });
}

//Modal shows db street how it works
function db_street_works() {
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/db_street_works/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#db_how_it_works_modal');
        }
    });
}

// Modal shows WPB how it works
function wpb_works() {
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/wpb_works/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#wpb_how_it_works_modal');
        }
    });
}

// Micro learning modal loads
function micro_modal(){
    $.ajax({
        method: 'GET',
        url: '/micro-learning-modal/',
        beforeSend: setHeader,
        success: function (response) {
            $("#common_base_modal").html('');
            $("#common_base_modal").html(response);
            show_bootstrap_modal('#micro_learning_modal');
        },
        error: function (response) {
            alert('Unable to process your request \n Please try again after some time.');
        }
    });
}

// Calendly modal loads
function calendly_modal(){
    $.ajax({
        method: 'GET',
        url: '/dashboard/calendly-modal/',
        beforeSend: setHeader,
        success: function (response) {
            $("#common_base_modal").html('');
            $("#common_base_modal").html(response);
            show_bootstrap_modal('#calendly_how_it_works_modal');
        },
        error: function (response) {
            alert('Unable to process your request \n Please try again after some time.');
        }
    });
}

//Modal shows micro learning packages
function give_advice_how_it_works() {
    var token = csrf_token;
    $.ajax({
        type: "GET",
        url: "/dashboard/give_advice_how_it_works/",
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#give_advice_how_works');
        }
    });
}

//Modal shows all package details
function subscribe_package(pkg_type, sub_cat_id, wallet, body_id) {
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/subscribe/subscribe-package-order/",
        data: {pkg_type : pkg_type, sub_cat_id:sub_cat_id, wallet:wallet},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#'+body_id).html('');
            $('#'+body_id).html(response);
            $('#payment').submit();
        }
    });
}

//Submit payment summary
function payment_summary(pkg_type, sub_cat_id, body_id) {
    var token = csrf_token;
    $.ajax({
        type: "POST",
        url: "/subscribe/payment-summary-details/",
        data: {pkg_type : pkg_type, sub_cat_id:sub_cat_id},
        beforeSend: function(request){
            request.setRequestHeader("X-CSRFToken" , token);
        },
        success: function(response){
            $('#'+body_id).html('');
            $('#'+body_id).html(response);
        }
    })
}

// Modal opens identity pack modal
identity_pack.on('click', function(e){
    $.ajax({
        type:"GET",
        url:"/subscribe/load-identity-pack/",
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken",csrf_token);
        },
        success: function(response){
            $('#dashboard_modal').html('');
            $('#dashboard_modal').html(response);
            show_bootstrap_modal('#identity_pack_list_modal');
        }
    });
});

//Modal downloads crisil certificate
function click_to_download(advisor_id) {
    var token = csrf_token;
    var w=window.open("/signup/crisil_certificate_pdf/",'_blank');
    w.focus();
}

// modify the domain
function calendly_domian() {
    var calendly_link = $('#id_calendly').val();
    var re = new RegExp(/^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/);
    if (!calendly_link.match(re)) {
        $("#help-text-calendly").html('Please Enter valid URL');
        $("#help-text-calendly").focus();
        return false;
    } else {
        if (!/^(f|ht)tps?:\/\//i.test(calendly_link)) {
            if (calendly_link.indexOf("www.") != 0) {
                $("#id_calendly").val('http://www.' + calendly_link);
            } else {
                $("#id_calendly").val('http://' + calendly_link);
            }
            $("#help-text-calendly").html('');
        } else if (!/((?:www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i.test(calendly_link)) {
            calendly_link = calendly_link.replace(/^http(s)?\:\/\//i, "");
            $("#id_calendly").val('http://www.' + calendly_link);
            $("#help-text-calendly").html('');
        }
        return true;
    }
}

// Save Calendly link
function save_link(){
    if (calendly_domian()) {
        $.ajax({
            type: "POST",
            url: "/dashboard/save_calendly_link/",
            data: {
                'link': $("#id_calendly").val()
            },
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (e, xhr, settings) {
                if (e.status == 200) {
                    show_alert(
                        'success',
                        'calendly-link-modal',
                        '<p>Calendly link added successfully.</p>'
                    );
                window.location.reload();
                }else{
                    show_alert(
                        'warning',
                        'calendly-link-modal',
                        '<p>Unable to save the link, Please try again later.</p>'
                    );
                }
            }
        });
    }else{
        show_alert(
            'warning',
            'calendly-link-modal',
            '<p>Please enter the link in proper format.</p>'
        );
    }
}
$(document).ready(function(){
    $("#hub_menu").addClass("active");
  })