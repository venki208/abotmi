var token = $("#id_csrf_token").val();
var search_button = $("[name='search_button']");
var search_form = $("#id_advisor_firm_form");
$(document).ready(function() {
    $("input[name='mobile']").intlTelInput({
        nationalMode: false,
        initialCountry: user_agent_country,
        separateDialCode: true,
        autoPlaceholder: "off",
    });
});

function validate_claimit_form() {
    missed_form_field = 0;
    var mobile_number = validate_field_onkeypress('id_advisor_mobile', 'help_advisor_mobile', 'Mobile Number');
    var email_id = validate_field_onkeypress('id_advisor_email', 'help_advisor_email', 'Email ID');
    var name = validate_field_onkeypress('id_advisor_name', 'help_advisor_name', 'Name');
    if(name !=0
        || mobile_number != 0
        || email_id != 0){
            return false;
    }else{
        return true;
    }
}

function show_success_message(message) {
    $("#claim_it_form").trigger('reset');
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-success');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
}

function show_error_message(message) {
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-danger');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
}

function show_warning_message(message) {
    $("#id_success_alert").removeClass();
    $("#id_success_alert").addClass('alert alert-warning');
    $("#id_success_alert").html('');
    $("#id_success_alert").html(message);
}

function show_conformation_alert(email) {
    $("#id_advisor_conformation").removeClass('hide');
    $("#save_member_data").prop('disabled', true);
    $("#id_save_continue_add_member").prop('disabled', true);
    $("#id_map_client_button").attr('onclick',  'accept_mapping("'+email+'",'+'"'+'accepted'+'"'+');');
    $("#id_cancel_client_button").attr('onclick', 'accept_mapping("'+email+'",'+'"'+''+'"'+');');
}

function show_claim_it_modal(advisor_id){
    $("#id_save_changes").attr('onclick', 'claim_it("'+advisor_id+'")');
    $("#claim_it_modal").modal({
        show : true,
        backdrop: 'static',
        keyboard: false
    });
}

function claim_it(advisor_id){
    var is_valid = validate_claimit_form();
    if(is_valid){
        if(advisor_id){
            disable_button('id_save_changes','Please Wait..');
            var email = $("#id_advisor_email").val();
            $.ajax({
                url : '/advisor_check/check_advisor/',
                type:'POST',
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken",token);
                },
                data:{
                    advisor_id : advisor_id,
                    name : $("#id_advisor_name").val(),
                    email : email,
                    mobile : $("#id_advisor_mobile").val()
                },
                success: function(response){
                    enable_button('id_save_changes','Claim It');
                    if(response.response == 'success'){
                        show_success_message('<strong>Your Details are matching.</strong>&nbsp;Please enter OTP which we have sent to '+'<strong>'+email+'</strong>');
                        add_values_to_hidden_fields(advisor_id);
                    }else{
                        show_error_message('<strong>Please Check your details with another card</strong>');
                    }
                },
                error: function(response) {
                    alert('we are unable to claim it now. please try again after some time');
                }
            });
        }else{
            alert('unable to procees');
        }
    }
}

function verify_otp(input_id) {
    if($("#"+input_id).val() != ''){
        disable_button('id_otp_submit','Please Wait..');
        var advisor_check_id = $("#id_hidden_advisor_id").val();
        $.ajax({
            type: 'POST',
            url:'/advisor_check/create_advisor/',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken",token);
            },
            data: {
                otp : $("#id_otp").val(),
                advisor_id : advisor_check_id
            },
            success: function(response){
                if(response != 'unable to create'){
                    cancel_modal();
                    hide_divs(advisor_check_id);
                    enable_button('id_save_changes','Claim It');
                    $("#claim_it_success_modal").modal('show');
                    $("#claim_success_"+advisor_check_id).each(function () {
                        $(this).removeClass('hide');
                    });
                }else{
                    enable_button('id_otp_submit','Verify OTP');
                    $("#help_id_otp").html('Invalid OTP');
                }
            },
            error: function(response){
                alert('uanble to create');
            }
        });
    }else{
        $("#help_id_otp").html('Invalid OTP');
    }
}

function hide_divs(advisor_check_id) {
    var div_ids = ['button_', 'id_title_', 'id_pending_'];
    for (var i = 0; i < div_ids.length; i++) {
        $("#"+div_ids[i]+advisor_check_id).addClass('hide');
    }
}

function add_values_to_hidden_fields(advisor_id) {
    $("#otp_block").removeClass('hide');
    $("#help_id_otp").html('');
    $("#id_claim_footer").addClass('hide');
    $("#advisor_block").addClass('hide');
    $("#id_hidden_advisor_id").val(advisor_id);
}

function disable_button(id, text) {
    $("#"+id).html(text);
    $("#"+id).attr('disabled', 'true');
}
function enable_button(id, text) {
    $("#"+id).removeAttr('disabled');
    $("#"+id).html(text);
}

function cancel_modal(){
    var claim_modal_ids = ['id_mobile', 'id_email', 'id_name'];
    enable_button('id_save_changes','Claim It');
    $("#claim_it_modal").modal('hide');
    $("#id_success_alert").addClass('hide');
    $("#otp_block").addClass('hide');
    $("#advisor_block").removeClass('hide');
    $("#id_claim_footer").removeClass('hide');
    for (var i = 0; i < claim_modal_ids.length; i++) {
        $("#help_"+claim_modal_ids[i]).html('');
        $("#"+claim_modal_ids[i]).removeClass('not_valid');
    }
}

function get_advisor_information(id){
    if (id){
        $.ajax({
            type : 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken",token);
            },
            url : '/advisor_check/get_advisor_information/',
            data : {
                'advisor_id' : id
            },
            success: function (response) {
                $("#id_additional_table_div_"+id).html('');
                if (response.response == 'success'){
                    $("#id_additional_table_div_"+id).append(
                        '<tr class="table-header"><th colspan="2" class="table-heading">Personal Certification</th></tr>'
                    );
                    for(i = 0; i<response.registrations.length; i++){
                        $("#id_additional_table_div_"+id).append(
                            '<tr><td class="division left-divison">'+response.registrations[i].registration_type+'</td><td class="division">'+response.registrations[i].registration_id+'</td></tr>'
                        );
                    }
                }else if(response.response == 'result_not_found'){
                    $("#id_additional_table_div_"+id).append(
                        '<tr class="table-header"><th colspan="2" class="table-heading">Personal Certification</th></tr><tr><td>No Additional data found.</td></tr>'
                    );
                }
                if($("#id_additional_div_"+id).hasClass('hide') == true){
                    $("#id_additional_div_"+id).removeClass('hide');
                    $("#more_"+id).addClass('fa-rotate-91');
                    $("#main_"+id).addClass('zoom');
                }else{
                    $("#id_additional_div_"+id).addClass('hide');
                    $("#more_"+id).removeClass('fa-rotate-91');
                    $("#main_"+id).removeClass('zoom');
                }
            },
            error: function (response) {
                alert('Unable to fetch information. Please try again later');
            }
        });
    }
}
$("#id_name, #id_mobile, #id_email, #id_location, #id_firm").on('keyup keydown',function() {
    var help_id = $('#'+this.id).closest(".form-group").find('.help-block')[0].id;
    var field_name = '';
    if (this.id == 'id_name'){
        field_name = 'Name';
    }else if(this.id == 'id_mobile'){
        field_name = 'Mobile Number';
    }else if(this.id == 'id_email'){
        field_name = 'Email';
    }else if(this.id == 'id_location'){
        field_name = 'Location';
    }else if(this.id == 'id_firm'){
        field_name = 'Firm';
    }
    var is_valid = validate_field_onkeypress(this.id, help_id, field_name);
});


function validate_search_form(){
    var is_valid_name = validate_field_onkeypress('id_name', 'help_id_name', 'Name');
    var is_valid_mobile = validate_field_onkeypress('id_mobile', 'help_id_mobile', 'Mobile Number');
    var is_valid_email = validate_field_onkeypress('id_email', 'help_id_email', 'Email');
    var is_valid_location = validate_field_onkeypress('id_location', 'help_id_location', 'Location');
    var is_firm_name = validate_field_onkeypress('id_firm', 'help_id_firm', 'Firm Name');
    if(is_valid_name !=0
        || is_valid_mobile != 0
        || is_valid_email != 0
        || is_valid_location != 0
        || is_firm_name !=0){
            return false;
    }else{
        return true;
    }
}


function return_data(){
    var name_value = '';
    var mobile_value = '';
    var email_value = '';
    var location_value = '';
    var firm_value = '';
    var missed_field = 0;
    name_value = $("#id_name").val();
    mobile_value = $("#id_mobile").val();
    email_value = $("#id_email").val();
    location_value = $("#id_location").val();
    firm_value = $("#id_firm").val();
    if(name_value != '' || mobile_value != '' || email_value != ''
    || location_value != '' || firm_value != ''){
        $("#id_validation_msg").html('');
        missed_field = 0;
    }else{
        missed_field = 1;
        $("#id_validation_msg").html('Please Enter Any One of Above');
    }
    if (firm_value != ''){
        var is_firm_name = validate_field_onkeypress('id_firm', 'help_id_firm', 'Firm Name');
        if(is_firm_name != 0){
            missed_field = 1;
        }
    }
    if(location_value != ''){
        var is_valid_location = validate_field_onkeypress('id_location', 'help_id_location', 'Location');
        if(is_valid_location !=0){
            missed_field = 1;
        }
    }
    if(email_value != ''){
        var is_valid_email = validate_field_onkeypress('id_email', 'help_id_email', 'Email');
        if(is_valid_email != 0){
            missed_field = 1;
        }
    }
    if(mobile_value != ''){
        var is_valid_mobile = validate_field_onkeypress('id_mobile', 'help_id_mobile', 'Mobile Number');
        if(is_valid_mobile != 0){
            missed_field = 1;
        }
    }
    if(name_value != ''){
        var is_valid_name = validate_field_onkeypress('id_name', 'help_id_name', 'Name');
        if(is_valid_name != 0){
            missed_field = 1;
        }
    }
    if(missed_field == 0){
        $("#id_validation_msg").html('');
    }
    else{
        missed_field = 1;
    }
    return {
        'name' : name_value,
        'mobile' : mobile_value,
        'email' : email_value,
        'location' : location_value,
        'firm' : firm_value,
        'missed_field': missed_field
    };
}

search_button.on('click', function(e){
    var data = return_data();
    if(data['missed_field'] == 0){
        search_form.submit();
    }
});

function navigate_to_search_page(id){
    $("#id_dynamic_page_no").val(id);
    $("#hidden_page_form").submit();
}

function claimed_modal() {
    $("#alreadyClaimedModal").modal('show');
}

$('select[name="category"]').change(function () {
    if ($(this).val()) {
        $('#id_firm').val('');
        $('.firm_name_div').addClass('hide');
    } else {
        $('.firm_name_div').removeClass('hide');
    }
});

function navigate_page(elem, page_type){
    $.ajax({
        method: 'POST',
        url: '/advisor_check/get_advisor_navigation_url/',
        beforeSend: setHeader,
        data: {
            ad_chk_id: $(elem).attr('adv_id'),
            page_type: page_type,
            chk_country: $(elem).attr('chk_country')
        },
        success: function (response) {
            if(response != 204 && response != 400 ){
                window.open(response, "_blank");
                window.focus();
            }
            else{
                alert('Unable to View the profile. \n Please try again after some time');
            }
        },
        error: function(response){
            alert('Unable to Process your request \n Please try again after some time');
        }
    });
}

function connect_advisor(elem){
    var ws = get_websocket();
    if(ws == undefined){
        ws = create_websocket_connection();
    }
    var id= $(elem).attr('adv_id');
    var chk_country = $(elem).attr('chk_country');
    $.ajax({
        method: 'POST',
        url: '/advisor_check/connect_advisor/',
        beforeSend: setHeader,
        data: {
            advisor_id: id,
            page_type: 'connect',
            chk_country: chk_country
        },
        success: function (response) {
            if (response.status_code == 200) {
                var d = {'command':'send', 'room':1,'data':'sending from websocket','advisor_id':response.advisor_id}
                ws.send(d)
                show_alert(
                    'success',
                    '',
                    "<p>You're now being connected with the advisor.</p>"
                );
            }
            else if(response.status_code == 204){
                if(response.status_txt == 'email_not_found'){
                    show_alert(
                        'warning',
                        '',
                        '<p>Email not found unable to send Email</p>'
                    );
                }else{
                    show_alert(
                        'error',
                        '',
                        '<p>Unable to Process your request \n Please try again after some time</p>'
                    );
                }
            }
            else{
                show_alert(
                    'error',
                    '',
                    '<p>Unable to Process your request \n Please try again after some time</p>'
                );
            }
        },
        error: function (response) {
            show_alert(
                'error',
                '',
                '<p>Unable to Process your request \n Please try again after some time</p>'
            );
        }
    });
}

function get_advice_page(elem){
    var id= $(elem).attr('adv_id');
    var category_name = $(elem).attr('category_name');
    $.ajax({
        method: 'POST',
        url: '/advisor_check/connect_advisor/',
        beforeSend: setHeader,
        data: {
            advisor_id: id,
            page_type: 'connect',
            category_name: category_name
        },
        success: function (response) {
            if (response.status_code == 200) {
                alert("You're now being connected with the advisor.");
            }
            else if(response.status_code == 204){
                if(response.status_txt == 'email_not_found'){
                    alert('Email not found unable to send Email');    
                }else{
                    alert('Unable to Process your request \n Please try again after some time');    
                }
            }
            else{
                alert(
                    'Unable to Process your request \n Please try again after some time');
            }
        },
        error: function (response) {
            alert('Unable to Process your request \n Please try again after some time');
        }
    });
}
