var token = $("#id_csrf_token").val();
var yes_button = $("[name='fin_adv']");
var no_button = $("[name='not_fin_adv']");
var reg_financial_opt = $("#id_reg_option");
var country_type_opt = $("#id_country_type");
var get_card_btn = $("[name='search_certification']");
var card_form = $("#card_form");
var save_card_form = $("#save_card_form");
var claim_btn = $("[name='claim_btn']");
var search_certification_btn = $("[name='search_certification']");
var cert_plceholder_type = '';
var fin_question_block = $("#fin_question_block");
var expertise_plus_button = $(".expert-btn");
var expertise_additional_block = $("#id_expert_additional_block");

if (is_advisor_found){
    if(card_user_profile_id == 'None' || card_user_profile_id == ''){
        load_bootstrap_modal("#advisorRegistrationModal");
        $('.container').removeClass('blur');
    }else {
        $("#advisor_container_block").empty();
        $("#advisor_container_block").html('<center><h2>You Claimed Your card already</h2></center>');
    }
}else{
    load_bootstrap_modal("#advisorRegistrationModal");
    $('.container').removeClass('blur');
}

function show_claim_it_modal(card_id) {
    load_bootstrap_modal("#advisorCheckCardModal");
    $('.container').removeClass('blur');
    $("[name='advisor_check_card_id']").val(card_id);
}

no_button.on('click', function(e){
    $("#advisorRegistrationModal").modal('hide');
    $("[name='certification_type']").val(reg_financial_opt.val());
    $("[name='certification_id']").val();
    $("[name='country_type_val']").val('');
    claim_btn.html('CREATE');
    show_claim_it_modal('');
    // need to remove once functionality freeze.
    // $("#advisorRegistrationModal").modal('hide');
    // $("#not_certified_modal").modal('show');
});

yes_button.on('click', function (e) {
    var validation_result = validate_expertise_form('id_expert_additional_block');
    if(validation_result){
        $("#options_block").removeClass('none');
    }
});

country_type_opt.on('change', function(e) {
    if(this.value){
        if(this.value == 'IN'){
            reg_financial_opt.removeClass('none');
        }else{
            reg_financial_opt.addClass('none');
            if (this.value == 'SG'){
                cert_plceholder_type = 'Member Number';
            } else if(this.value == 'US'){
                cert_plceholder_type = 'CRD';
            } 
            else{
                cert_plceholder_type = 'License ID';
            }
            $("#id_reg_no")
                .removeClass('none')
                .attr('placeholder', 'Please Enter '+cert_plceholder_type)
                .focus();
        }
    }else{
        reg_financial_opt.addClass('none');
        $("#id_reg_no")
            .addClass('none')
            .val('');
    }
});

reg_financial_opt.on('change', function (e) {
    if(this.value){
        if(this.value == 'AMFI'){
            cert_plceholder_type = 'ARN Number';
        }else if(this.value == 'BSE'){
            cert_plceholder_type = 'Clearing Number';
        }else if(this.value == 'CA'){
            cert_plceholder_type = 'Registration ID';
        }else if(this.value == 'IRDA'){
            cert_plceholder_type = 'URN Number';
        }else{
            cert_plceholder_type = 'Registration Number';
        }
        $("#id_reg_no")
            .removeClass('none')
            .attr('placeholder', 'Please Enter '+cert_plceholder_type)
            .focus();
    }else{
        $("#id_reg_no")
            .addClass('none')
            .val('');
    }
});

$("#id_reg_no").on('keyup keydown', function () {
    var help_id = $('#'+this.id).closest(".form-group").find('.help-block')[0].id;
    var field_name = cert_plceholder_type;
    var is_valid = validate_field_onkeypress(this.id, help_id, field_name);
    if (is_valid != 1){
        search_certification_btn.removeClass('none');
    }else{
        search_certification_btn.addClass('none');
    }
});

claim_btn.on('click', function(e){
    $("[name='advisors_city']").val($("#id_city").val());
    var reg = /^([\s.]?[a-zA-Z]+)+$/;
    var is_valid = validate_field_onkeypress('id_city', 'help_city', 'city');
    if (is_valid != 1) {
        if (!reg.test($("#id_city").val())) {
            $("#help_city").html('Please enter valid city name');
            return false;
        }
        $("#save_card_form").submit();
    }
});

search_certification_btn.on('click', function (e) {
    var validation_result = validate_expertise_form('id_expert_additional_block');
    if(validation_result){
        var registration_no = $("#id_reg_no").val();
        var advisors_city = $("#id_city").val();
        $.ajax({
            type: 'POST',
            url: '/advisor_check/get_certified_card/',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data:{
                'country_type': country_type_opt.val(),
                'certificate_type': reg_financial_opt.val(),
                'certificate_id': registration_no,
                'advisors_city': advisors_city
            },
            success: function (response) {
                $("#advisorRegistrationModal").modal('hide');
                $("[name='certification_type']").val(reg_financial_opt.val());
                $("[name='certification_id']").val(registration_no);
                $("[name='country_type_val']").val(response.country_type);
                $("[name='advisors_city']").val($("#id_city").val());
                show_claim_it_modal(response.card_id);
                if(response.status_code == 200){
                    claim_btn.html('CREATE');
                }else if(response.status_code == 302){
                    $('.match_text').html("We have a <strong>Profile Match </strong> for you. Claim it!");
                }
            },
            error: function (response) {
                alert('Unable to process your request \n Please Try Again Later');
            }
        });
    }
});

// calling function on click of add button
expertise_plus_button.on('click', function(e){
    var selected_value = $(this).parent().find('select').val();
    var validation_result = validate_expertise_form('id_expert_additional_block');
    if (validation_result){
        if (selected_value != 'Select'){
            if (selected_value != 'Others') {
                $("#" + $(this).parent().find('select').attr('id') + " option:selected").remove();
            }
            expertise_additional_block.append(return_new_tag(selected_value));
            expertise_additional_block
                .find('a').addClass('remove_btn')
                .bind('click', remove_expertise)
                .parent().find('.help-block')[0].innerHTML = '';
            $(this).parent().find('.help-block').html('');
            $(this).parent().find('select').val('Select');
            // showing yes or no question
            $("#fin_question_block").removeClass('hide');
        }else{
            $(this).parent().find('.help-block').html('Please select Your Expertise');
        }
        get_details();
    }
});

// attaching click event to remove button
$(".remove_btn").on('click', function(e){
    remove(e);
});

// removing the option
function remove_expertise(e){
    var removed_otpion = $(this).parent().find('select').val();
    if(removed_otpion != 'Others'){
        $("#id_expertise_opt").append(
            '<option value=' + removed_otpion + '>' + removed_otpion + '</option>'
        );
    }
    $(this)
        .closest('.row')
        .remove();
    // hiding yes or no question
    if ($(this).parent().find('select').length < 1){
        $("#fin_question_block").addClass('hide');
    }
}

// validating the expertise form
function validate_expertise_form(parent_id){
    var missed_fields = 0;
    $($("#"+parent_id).find(".form-control").get().reverse()).each(function () {
        if (this.value == 'Select' || this.value == '' || this.value == undefined){
            $(this).parent().find('.help-block').html('This field is required');
            missed_fields = 1;
        }
    });
    if(missed_fields == 0){
        return true;
    }else{
        return false;
    }
}

// function for creating new select tag
function return_new_tag(options_array){
    var others_div = '';
    if(options_array == 'Others'){
        others_div = '<textarea class="form-control" name="others[]" autofocus></textarea>';
    }else{
        others_div = '<input class="hidden form-control" name="others[]" value = "true">';
    }
    return '<div class="row">'+
                '<label for="exampleInputName2" class="col-sm-2 text-right" style="line-height: 30px;">I am a</label>'+
                '<div class="col-sm-8">'+
                    '<div class="form-group">'+
                        '<select name="expertise_otp[]" id="" class="form-control" readonly>'+
                            '<option value='+'"'+options_array+'"'+'>'+options_array+'</option>'+
                        '</select>'+
                        others_div+
                        '<span class="help-block"></span>'+
                    '</div>'+
                '</div>'+
                '<a class="btn additional-button expert-btn col-md-2">'+
                    '<i class="fa fa-minus-circle"></i>'+
                '</a>'+
            '</div>';
}

// function for get all expertise data and serilize
function get_details(){
    var values = $("#id_expert_parent_row").find('.form-control').serializeArray();
    $("input[name='expertise']").val(JSON.stringify(values));
}

$('[name="no_card_back_btn"]').on('click', function(){
    $("#not_certified_modal").modal('hide');
    $("#advisorRegistrationModal").modal('show');
});


function load_bootstrap_modal(elem){
    $(elem).modal({
        show: true,
        keyboard: false,
        backdrop: false
    });
}